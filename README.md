# ambition
(P.I. Joe Jarvis)


### Installation

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
    
    # install requirements
    cd ~/source/ambition
    pip install -r requirements.txt  # or requirements_production.txt
    
    # create database
    mysql -u <user> -p -Bse 'create database ambition character set utf8;'
    
    # populate timezone table
    mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
    
    # migrate
    python manage.py migrate
    
    # import required data
    python manage.py import_randomization_list
    python manage.py import_holidays
    
    # check for any obvious issues
    python manage.py check


### Production setup

The production server uses `requirements_production.txt` and the "live" settings in `ambition.settings.live.xxx`, for example, `ambition.settings.live.gaborone`.

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
