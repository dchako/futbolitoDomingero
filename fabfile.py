import re
import os
from fabric.api import local, task
from fabric.context_managers import settings, shell_env

PRODUCTION = 'prod'
STAGGING   = 'stg'  
DEFAULT    = 'default'
STATIC     = 'static'
HEROKU     = 'heroku'
PATH       = 'path'


STORAG = 'FILE_STORAGE'
ACCESS = 'GS_ACCESS_KEY_ID'
SECRET = 'GS_SECRET_ACCESS_KEY'
BUCKET = 'GS_STORAGE_BUCKET_NAME'

# Collect Static Env for production

MAIN_PRODUCTION = { 
    STORAG: "django-google-storage.storage.GoogleStorage",
    ACCESS: "accesss",
    SECRET: "secrey",
    BUCKET: "stg.futbolito-domingero.com.ar",
}

MIRROR_PRODUCTION = MAIN_PRODUCTION
MIRROR_STAGGING   = MAIN_PRODUCTION


EXTERNAL_APPS = {DEFAULT    :{PRODUCTION: { HEROKU: 'runplayers',       STATIC: MAIN_PRODUCTION },
                              },
                }

APP         = EXTERNAL_APPS[DEFAULT][PRODUCTION]
HEROKU_APP  = EXTERNAL_APPS[DEFAULT][PRODUCTION][HEROKU]

DUMP_FILE = 'dump.sql'



def heroku_run(cmd, *args, **kwargs):
    heroku_app = kwargs.pop('heroku_app', HEROKU_APP)
    app = '-a {name}'.format(name=heroku_app)
    cmd = ' '.join(['heroku', cmd, app])

    return local(cmd, *args, **kwargs)


hrun = heroku_run


@task
def dumpdb():
    """Generate a dump of a remote database"""
    out = hrun('pg:backups capture', capture=True)
    backup_id = re.search('b\d{3}', out).group()

    backup_url = hrun('pg:backups public-url {id}'.format(id=backup_id), capture=True)

    local('wget "{url}" -O dump.sql'.format(url=backup_url))


@task
def loaddb():
    with settings(warn_only=True):
        local('pg_restore --clean -O -h localhost -U postgres -d futbolito-domingero_prod {}'. \
        format(DUMP_FILE))


@task
def bootstrap():
    # Get latest version of database
    dumpdb()
    loaddb()

    # Grab homepage images and store them in staticfiles directory