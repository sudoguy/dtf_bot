python3 manage.py migrate
python3 manage.py collectstatic
uwsgi --ini uwsgi.ini
