cd /src/application/
python3 manage.py makemigrations
python3 manage.py migrate
sed -i 's/DB_NAME/PRDB_NAME/g' /src/application/django_app/.env
echo 'DB_NAME="bloglocalv1"' >> /src/application/django_app/.env
python3 /src/application/manage.py dumpdata auth > /src/application/initial_data_auth.json
cp /src/application/django_app/env /src/application/django_app/.env
python3 /src/application/manage.py loaddata /src/application/initial_data_auth.json
nohup python3 manage.py runserver 0.0.0.0:4000 > /var/log/django_app.log 2>&1 &