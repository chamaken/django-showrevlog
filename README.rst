=================
django-showrevlog
=================

This is a fork of `django-log-file-viewer
<https://github.com/garmoncheg/django-log-file-viewer>`_ to work with
Django-1.11 and to show log files in reverse order.

Useful to add log files view functionality to your Django admin web site.
Instead of using database log files storage, it gives you ability to
store/view log files through GUI.  It requires a directory with Django log
files to function. E.g. directory structure::

    $ project_dir/logs/:
       applog.log
       applog.log.2012-09-22
       ...
       errors.log
       applog.log.2012-09-22
       ...


Quick start
-----------

1. Install an app and add it to your settings.py INSTALLED_APPS section::

     # settings.py:
     INSTALLED_APPS = (
         ...
         'showrevlog.apps.ShowRevLogConfig',
         ...
     )

2. Set UP 2 django variables in settings.py::

     # settings.py:
     SHOWREVLOG_DIR = os.path.join(BASE_DIR, 'log')
     SHOWREVLOG_LINEXP = ('(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})'
                          '\s(?P<type>[A-Z]+)'
                          '\s\[(?P<source>[^:]+):(?P<line>[0-9]+)\]'
                          '\s(?P<process>[0-9]+)'
                          '\s(?P<message>.+)')

   Is a regex to parse your log file. It completely depends of your Django
   logging settings. And table column names (in a parsed logfile) depend from
   group names you provide in the regexp. To produce this log You may add this
   formatter to the website.::

     'formatters': {
          'normal': {
              'format': '%(asctime)s %(levelname)s [%(filename)s:%(lineno)s] %(process)d %(message)s'
          },
      },

3. And add urls to your main urls section::

     # urls.py:
     urlpatterns = [
         ...
         # Include this before admin to enable app admin url overrides
         # Note url must be the same as admin. This is required step
         url(r'^admin/showrevlog/', include('showrevlog.admin_urls', namespace='showrevlog')),
         url(r'^admin/', admin.site.urls),
         ...

4. Run `python manage.py migrate` to create the polls models.
   
5. Create superuser by `python manage.py createsuperuser`
   
6. Start the development server and visit
   http://127.0.0.1:8000/admin/
