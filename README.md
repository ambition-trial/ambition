# ambition
(P.I. Joe Jarvis)


### Installation

 See ambition/ubuntu.txt for required ubuntu packages

Decide on the user account for the installation. E.g. `django`. 

    sudo su django

    # create folders

    mkdir  ~/.venvs
    mkdir  ~/source
    
    # create VENV
    python3 -m venv ~/.venvs/ambition
    
    # activate VENV
    source ~/.venvs/ambition/bin/activate
    
    # update pip
    pip install -U pip ipython
    
    # clone main project
    cd ~/source/
    git clone https://github.com/ambition-trial/ambition.git
    
    # make log folder
    mkdir ~/source/ambition/log/
    
    # install requirements
    # GOTO section for "Test/UAT setup" or "Production setup", then proceed ...

    # create database
    # GOTO section on "mysql and settings", then proceed ...

    # migrate database
    python manage.py migrate --settings=ambition.settings.yourfile
    
    # import required data
    python manage.py import_randomization_list --settings=ambition.settings.yourfile
    python manage.py import_holidays --settings=ambition.settings.yourfile
    
    # check again
    python manage.py check --settings=ambition.settings.yourfile


### Test/UAT setup

... continued from Installation above
    
    # mysql.conf (see example below)
    sudo touch /etc/ambition/mysql.conf/uat.conf
    
    # install requirements
    cd ~/source/ambition
    pip install -r requirements.txt

    # make encryption KEY folder
    sudo mkdir -p /etc/ambition/test/crypto_fields
        
    # run check for a gaborone UAT site
    python manage.py check --settings=ambition.settings.test.gaborone-uat
    
    # confirm DB credentials
    cat /etc/


### Production setup

... continued from Installation above

    # install requirements
    cd ~/source/ambition
    pip install -r requirements_production.txt
    
    # make encryption KEY folder
    sudo mkdir -p /etc/ambition/live/crypto_fields
            
    # run check for a gaborone LIVE site
    python manage.py check --settings=ambition.settings.live.gaborone

### `mysql` and django `settings`

To run several instances of the `ambition` application on a single server, create a folder for the `.conf` files.

    sudo mkdir -p /etc/ambition/mysql.conf/

For each application create a `.conf` file

    sudo touch /etc/ambition/mysql.conf/uat.conf
    sudo touch /etc/ambition/mysql.conf/live.conf
    # ...

Your `.conf` file should look something like this:

    [client]
    host = 127.0.0.1
    port = 3306
    database = your_db_name
    user = your_mysql_user
    password = your_mysql_password
    default-character-set = utf8


In the application's django settings set the `read_default_file` OPTION of `DATABASES` to the correct mysql `.conf` file.

    MYSQL_DIR = os.path.join('/etc', APP_NAME, 'mysql.conf')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': os.path.join(MYSQL_DIR, 'uat.conf'),
            },
        },
    }

Create the database. Refer to your `.conf` file for the DB name. Assuming you chose `ambition` as the DB name.
    
    mysql -u <user> -p -Bse 'create database ambition character set utf8;'

Populate timezone table.

    mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql



#### /etc

For the live server, the settings file places Django's `SECRET_KEY` and `django-crypto-fields` encryption keys in `/etc/ambition/live`. The account used to load the system must have read access to these files.

    
### Logging for UAT and Production Servers
 
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

