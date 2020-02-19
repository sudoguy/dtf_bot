python3 manage.py migrate
python3 manage.py collectstatic --noinput
ddtrace-run uwsgi --ini uwsgi.ini
