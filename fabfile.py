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
MIRROR     = 'mirror'


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


EXTERNAL_APPS = { DEFAULT     :{ PRODUCTION: { HEROKU: 'runplayers',       STATIC: MAIN_PRODUCTION },
                                 MIRROR: True,
                               },
                 'runplayers' :{ PRODUCTION: { HEROKU: 'runplayers',      STATIC: MIRROR_PRODUCTION },
                                 MIRROR: True,
                               },
                }

APP         = EXTERNAL_APPS[DEFAULT][PRODUCTION]
HEROKU_APP  = EXTERNAL_APPS[DEFAULT][PRODUCTION][HEROKU]

DUMP_FILE = 'dump.sql'


@task
def app(application):
    """ 
        Configure which remote application to use

        f.e.    fab deploy:prod
                fab deploy:prod-lets
                fab deploy:prod-big
                fab deploy:prod-abm
    """
    global APP
    global VERSION
    global HEROKU_APP

    version = application.split('-')[0] if application and type(application) == str else ''
    app     = application.split('-')[1] if len(application.split('-')) >= 2 else DEFAULT

    if version not in [PRODUCTION, STAGGING]:
        raise ValueError("Invalid version option: {app}. Only support prod and stg".format(app=version))

    if app in EXTERNAL_APPS.keys():
        APP        = app
        VERSION    = version
        HEROKU_APP = EXTERNAL_APPS[app][version][HEROKU]
    else:
        raise ValueError("Invalid APP name: {app}".format(app=app))


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
        local('pg_restore --clean -O -h localhost -U postgres -d futbolitodomingero_prod {}'. \
        format(DUMP_FILE))


@task
def bootstrap():
    # Get latest version of database
    dumpdb()
    loaddb()

    # Grab homepage images and store them in staticfiles directory

@task
def push(remote=None, branch='master', heroku_app=HEROKU_APP):
    """Push the master branch to the remote application"""

    if remote:
        print "PUSH TO GITHUB \t Branch:{})".format(branch)
    else:
        print "PUSH TO HEROKU {} \t Branch:{}".format(heroku_app, branch)

    if remote:
        local('git push {remote} {branch}:{branch}'. \
        format(remote=remote, branch=branch))
    else:
        local('git push -f git@heroku.com:{app}.git {branch}:master'. \
        format(app=heroku_app, branch=branch))


@task
def deploy(application, branch='master'):
    """Deploy the given remote application"""
    app(application)

    if PRODUCTION in application:
        push(remote='origin', branch=branch) # Main repository

    if EXTERNAL_APPS[APP][MIRROR]:
        push(branch=branch, heroku_app=EXTERNAL_APPS[APP][VERSION][HEROKU])