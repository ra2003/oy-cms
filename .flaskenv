# {{ project_name }} environment variables
# Some values are auto-generated
# You can edit the existing ones and/or add new variables
{% set PROJECT_NAME = project_name|upper %}

FLASK_APP = "{{ project_name }}"
FLASK_ENV = "development"
{{ PROJECT_NAME }}_DEBUG = True
{{ PROJECT_NAME }}_SECRET_KEY = "{{ secret_key }}"
{{ PROJECT_NAME }}_DB_URI = 'sqlite:///db.sqlite'
{{ PROJECT_NAME }}_PASSWORD_SALT = "{{ password_sult }}"