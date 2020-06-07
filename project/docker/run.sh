cd /network_confrontation/src/web || exit 1
python manage.py migrate
python manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8085 --access-log /var/log/ms103_nc/daphne_access.log network_confrontation_web.asgi:application
