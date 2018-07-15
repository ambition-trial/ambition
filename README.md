# ambition

(P.I. Joe Jarvis)


### VENV Installation

See also [docker install](#docker-install)

There are three requirements files 

    requirements_dev.txt  # installs all in editable mode from your workspace 
    requirements_production.txt # installs each by tag
    requirements.txt  # installs each from develop branch (for ci / tests)

See `ambition/ubuntu.txt` for required ubuntu packages

Decide on the user account for the installation. E.g. ambition. 

    sudo su ambition

create folders

    mkdir  ~/.venvs
    mkdir -p ~/source/ambition/log/
    
create VENV

    python3 -m venv ~/.venvs/ambition
    
activate VENV

    source ~/.venvs/ambition/bin/activate
    
update pip

    pip install -U pip ipython
    
clone main project

    cd ~/source/ \
    && git clone https://github.com/ambition-trial/ambition.git

change to project folder

    cd ~/source/ambition

copy your .env file into the project root

    cp /some/path/to/.env ~/source/ambition/.env
    
install requirements, select the require file. See requirements options above.

    # pip install -r requirements.txt
    
    pip install -r requirements_production.txt

 create database and populate timezone table

    mysql -u <user> -p -Bse 'create database ambition character set utf8;' \
    && mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
    
migrate database

    python manage.py migrate
    
import required data

    python manage.py import_randomization_list \
    && python manage.py import_holidays
    
check
    
    python manage.py check


### Environment variables

Settings variables are store in the environment.

See [django-environ](https://github.com/joke2k/django-environ) and [12-factor-django](http://www.wellfireinteractive.com/blog/easier-12-factor-django/)

Place your .env file in the root of the project.

Available variables are:

#### secure values

    DATABASE_URL= # mysql://user:password@127.0.0.1:3306/database_name
    DJANGO_SECRET_KEY=
    MYSQL_ROOT_PASSWORD=

#### review these site specific variables in the django section
* `DJANGO_COUNTRY`
* `DJANGO_CUPS_SERVERS`
* `DJANGO_HOLIDAY_FILE`
* `DJANGO_LANGUAGES`
* `DJANGO_SITE_ID`
* `DJANGO_TIME_ZONE`

#### django and edc

    DJANGO_APP_NAME=
    DJANGO_ALLOWED_HOSTS= # localhost,127.0.0.1
    DJANGO_COUNTRY=
    DJANGO_CSRF_COOKIE_SECURE= # True
    DJANGO_CUPS_SERVERS=
    DJANGO_DASHBOARD_BASE_TEMPLATES=
    DJANGO_DASHBOARD_URL_NAMES=
    DJANGO_DEBUG=
    DJANGO_EMAIL_CONTACTS=
    DJANGO_ETC_DIR=
    DJANGO_EXPORT_FOLDER=
    DJANGO_FQDN= # clinicedc.org
    DJANGO_HOLIDAY_FILE=
    DJANGO_INDEX_PAGE=
    DJANGO_KEY_PATH=
    DJANGO_LAB_DASHBOARD_BASE_TEMPLATES=
    DJANGO_LAB_DASHBOARD_REQUISITION_MODEL=
    DJANGO_LAB_DASHBOARD_URL_NAMES=
    DJANGO_LANGUAGES= # en:English
    DJANGO_LANGUAGE_CODE= # en-us
    DJANGO_LABEL_TEMPLATE_FOLDER=
    DJANGO_LOGIN_REDIRECT_URL= # home_url
    DJANGO_MAIN_NAVBAR_NAME=
    DJANGO_OFFLINE_SERVER_IP=
    DJANGO_OFFLINE_FILES_REMOTE_HOST=
    DJANGO_OFFLINE_FILES_USER=
    DJANGO_OFFLINE_FILES_USB_VOLUME=
    DJANGO_RANDOMIZATION_LIST_FILE=
    DJANGO_REVIEWER_SITE_ID=
    DJANGO_SECURE_PROXY_SSL_HEADER= # (HTTP_X_FORWARDED_PROTO,https)
    DJANGO_SESSION_COOKIE_SECURE= # True
    DJANGO_SITE_ID=
    DJANGO_STATIC_ROOT=
    DJANGO_STATIC_URL= # /static/
    DJANGO_TIME_ZONE= # Africa/Gaborone
    DJANGO_USE_I18N= # True
    DJANGO_USE_L10N= # False
    DJANGO_USE_TZ= # True
    MYSQL_DATABASE=


### Logging
 
 If logging through syslog is implemented, you need to configure rsyslog.
 
    nano /etc/rsyslog.d/30-ambition.conf
 
 add this to the file
 
    # /etc/rsyslog.d/30-ambition.conf
    local7.*                                             /var/log/ambition.log
    & ~  # This stops local7.* from going anywhere else.

 restart rsyslog
 
    sudo service rsyslog restart
 
 view the log
 
    tail -n 25 -f /var/log/ambition.log

### Docker Install
