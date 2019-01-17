import pytest
import oy
from werkzeug.utils import import_string
from webtest import TestApp
from oy.boot.sqla import db as sqla_db
from oy.boot.security import user_datastore


@pytest.fixture(scope="module")
def app():
    app = oy.create_app(
        __name__,
        config=dict(
            SECRET_KEY="testing-secret-key",
            TESTING=True,
            DEBUG=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            SECURITY_PASSWORD_HASH="plaintext",
        ),
    )
    yield app


@pytest.fixture(scope="module")
def client(app):
    yield TestApp(app)


def create_user():
    admin_role = user_datastore.find_or_create_role("admin")
    return user_datastore.create_user(
        user_name="admin",
        email="admin@localhost.com",
        password="adminpass",
        roles=[admin_role],
    )


@pytest.fixture(scope="function")
def db(request, app):
    with app.app_context():
        sqla_db.create_all()
        user = create_user()
        sqla_db.session.commit()
        yield sqla_db
        sqla_db.drop_all()

