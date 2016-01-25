
from fabric.api import *
from fabric.colors import *
import sys

__root_dir = '/home/dha/workspace/testapp/'
__database_dir = __root_dir
__main_dir = '/home/dha/workspace/testapp/testapp'

env.hosts = ['funing@funing.co.kr']


def deploy():
    print(blue("==================================================="))
    print(blue("Funing Deploy"))
    with cd(__root_dir):
        print(magenta("STEP 1. git pull"))
        run('git pull')

    with cd(__main_dir):
        print(magenta("STEP 2. South Database Migration"))
        run('python manage.py migrate cms')
        print(magenta("STEP 3. Collect Static Files"))
        run('python manage.py collectstatic')
        print(magenta("STEP 4. Delete *pyc Files"))
        run('rm -f `find . -name "*pyc"`')
        print(magenta("STEP 5. Apache Restart"))
        sudo('service apache2 restart')
    print(blue("==================================================="))


def reboot():
    print(blue("==================================================="))
    print(blue("Funing Apache Restart"))
    with cd(__main_dir):
        print(magenta("STEP 1. Collect Static Files"))
        run('python manage.py collectstatic')
        print(magenta("STEP 2. Delete *pyc Files"))
        run('rm -f `find . -name "*pyc"`')
        print(magenta("STEP 3. Apache Restart"))
        sudo('service apache2 restart')
    print(blue("==================================================="))


def syncdb():
    print(blue("==================================================="))
    print(blue("SyncDb Start"))
    with cd(__root_dir):
        print(magenta("STEP 1. Delete SqliteFile"))
        run('rm -f cms.sqlite')

    with cd(__root_dir):
        print(magenta("STEP 2. DB Migrations"))
        run('python manage.py syncdb')
        run('python manage.py migrate cms')

    with cd(__root_dir):
        print(magenta("STEP 3. Grant To 777 SqliteFile"))
        run('chmod 777 cms.sqlite')

    print(blue("==================================================="))
    
print(magenta(sys.argv[1]))
  
if sys.argv[1] == "syncdb":
  
    syncdb();
    exit(1)