import os 
from tempfile import mkdtemp
from starlit import create_app
from starlit.boot.exts.sqla import db
from starlit_admin.plugin import AdminPlugin


TEMP_DIR = mkdtemp()  
UPLOADS_PATH = os.path.join(TEMP_DIR, "uploads")

if not os.path.exists(UPLOADS_PATH):
    os.mkdir(UPLOADS_PATH)

config = dict(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite",
    #EXPLAIN_TEMPLATE_LOADING=True,
    SECURITY_PASSWORD_SALT = '540SDW4426HCAER56546aDrw213d2a6b9a94e15b5d',
    UPLOADS_PATH=UPLOADS_PATH,
)

app = create_app('dev', config=config)
app.use(AdminPlugin)

with app.app_context():
    db.create_all()