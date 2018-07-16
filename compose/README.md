
create a docker droplet



log into your droplet and create a user account for the app

    useradd ambition
    usermod -aG docker ambition
    usermod -aG sudo ambition

log into your droplet as user `ambition`

    ssh ambition@example.com

The rest of the steps assume you are log into your droplet as user `ambition`

checkout the repo

    cd ~/
    git checkout -b develop git https://github.com/ambition-trial/ambition.git app 

make folders for the container volumes

    sudo mkdir -p /srv/ambition/data \
        && /srv/ambition/backup \
        && /srv/ambition/log \
        && /srv/ambition/export \
        && /srv/ambition/.etc/crypto_fields \
        && /srv/ambition/static
    
copy your `.env` file into the app root

    cp /some/path/to/.env ~/app/ambition/.env

or `scp`
    
    scp .production ambition@example.com:~/app/.env

edit `~/app/ambition/.env` file as required, for example

    # DB and SECRET_KEY
    DATABASE_URL=mysql://user:password@127.0.0.1:3306/ambition_new
    DJANGO_SECRET_KEY=
    MYSQL_ROOT_PASSWORD=password
    MYSQL_DATABASE=
    
    # find these site specific and update as required
    DJANGO_COUNTRY=
    DJANGO_CUPS_SERVERS=
    DJANGO_LANGUAGES=
    DJANGO_SITE_ID=
    DJANGO_TIME_ZONE=
    
build images for `ambition_production` and `mysql` and bring them `up`
    
    docker-compose -f compose/local.yml build \
    && docker-compose -f compose/local.yml up
    
>>> Note: if you need to generate keys set DJANGO_AUTO_CREATE_KEYS=True in the `.env`, `docker-compose up`, change back to false and `docker-compose up` again
    
In another shell, log into the container

    docker exec -it ambition_production /bin/bash

... run migrations and other management commands as required
    
    python manage.py migrate
    python manage.py import_holidays
    python manage.py migrate import_randomization_list 

While still in the container, run check

    python manage.py check

Start runserver

    python manage.py runserver 0.0.0.0:8000
    
