import os
import sys
 
path = '/home/dha/workspace/testapp/testapp'    
if path not in sys.path:
     sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'testapp.settings' 

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler
