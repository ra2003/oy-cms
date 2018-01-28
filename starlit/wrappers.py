from importlib import import_module
from warnings import warn
from flask import Flask, Blueprint
from flask.config import Config
from starlit.util.helpers import find_modules, import_modules


class StarlitConfig(Config):
    def from_package_defaults(self, package_name):
        for modname in find_modules(package_name):
            try:
                imported = import_module("%s.defaults" %(modname))
                self.from_object(imported)
            except ImportError:
                continue


class StarlitModule(Blueprint):

    def __init__(self, name, import_name, builtin=True, *args, **kwargs):
        self.name = name
        if builtin:
            self.name = "starlit-{}" .format(self.name)
        super(StarlitModule, self).__init__(self.name, import_name, *args, **kwargs)
        self.settings_providers = []
        self.finalize_funcs = []

    def settings_provider(self, func):
        self.settings_providers.append(func)
        def wrapped(*a, **kw):
            return func(*a, **kw)
        return wrapped

    def after_setup(self, func):
        self.finalize_funcs.append(func)
        def wrapped(*a, **kw):
            return func(*a, **kw)
        return wrapped

    def get_provided_settings(self):
        for provider in self.settings_providers:
            yield provider()


class Starlit(Flask):
    config_class = StarlitConfig

    def __init__(self, *args, **kwargs):
        super(Starlit, self).__init__(*args, **kwargs)
        self.blueprint_packages = []
        self.plugins = {}

    def find_blueprints(self, basemodule):
        for module in import_modules(basemodule):
            modname = module.__name__
            if modname in self.config['EXCLUDED_MODULES']:
                continue
            starlit_modules = (v for k,v in module.__dict__.items() if isinstance(v, StarlitModule))
            if starlit_modules and modname not in self.blueprint_packages:
                self.blueprint_packages.append(modname)
            for bp in starlit_modules:
                yield bp

    def provided_settings(self):
        opts = []
        for bp in self.blueprints.values():
            provider = getattr(bp, 'get_provided_settings', None)
            if provider is None:
                continue
            for provided in  provider():
                for p in provided:
                    p.blueprint = bp
                opts.extend(provided)
        return opts

    def use(self, plugin, *args, **kwargs):
        plugin = plugin()
        self.plugins[plugin.identifier] = plugin
        plugin.init_app(self, *args, **kwargs)
        if plugin.needs_blueprint_registration:
            self.register_blueprint(plugin)
        return plugin
