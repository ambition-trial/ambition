|pypi| |travis| |coverage|


Ambition Edc
------------
(P.I. Joe Jarvis)

http://www.isrctn.com/ISRCTN72509687


VENV Installation
=================

See also [docker install](#docker-install)

There are three requirements files 

* requirements_dev.txt  # installs all in editable mode from your workspace 
* requirements_production.txt # installs each by tag
* requirements.txt  # installs each from develop branch (for ci / tests)

See ``ambition-edc/ubuntu.txt`` for required ubuntu packages

Decide on the user account for the installation. E.g. edc. 


.. code-block:: bash

    sudo su edc

create folders

.. code-block:: bash

    mkdir  ~/.venvs
    mkdir -p ~/source/ambition-edc/log/
    
create VENV

.. code-block:: bash

    python3 -m venv ~/.venvs/ambition-edc
    
activate VENV

.. code-block:: bash

    source ~/.venvs/ambition-edc/bin/activate
    
update pip

.. code-block:: bash

    pip install -U pip ipython
    
clone main project

.. code-block:: bash

    cd ~/source/ \
    && git clone https://github.com/ambition-trial/ambition-edc.git

change to project folder

.. code-block:: bash

    cd ~/source/ambition-edc

copy your .env file into the project root

.. code-block:: bash

    cp /some/path/to/.env ~/source/ambition-edc/.env

    
install requirements, select the require file. See requirements options above.

.. code-block:: bash

    # choose one
    pip install -r requirements/stable.txt

    pip install -r requirements/production.txt
 
 create database and populate timezone table

    mysql -u <user> -p -Bse 'create database ambition character set utf8;' \
    && mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
    
migrate database

.. code-block:: bash

    python manage.py migrate
    
import required data

.. code-block:: bash

    python manage.py import_randomization_list \
    && python manage.py import_holidays
    
check
    
.. code-block:: bash

    python manage.py check


Environment variables
=====================

Settings variables are store in the environment.

See django-environ_ and 12-factor-django_.

Place your ``.env`` file in the root of the project.

.. note:: Available variables are listed in env.sample_.



Docker Install
==============

Work in progress....

Install Docker_ Compose.

create a droplet for the host

    ...


log into your host and create a user account for the app

.. code-block:: bash

    useradd ambition
    usermod -aG docker ambition
    usermod -aG sudo ambition

log out and log back in as user `ambition`

.. code-block:: bash

    ssh ambition@example.com

The rest of the steps assume you are logged into your host as user `ambition`

checkout the main ambition repo into `app`

.. code-block:: bash

    cd ~/
    git checkout -b develop git https://github.com/ambition-trial/ambition.git app 

make a folder on your host for the container volumes

.. code-block:: bash

    sudo mkdir -p /srv/ambition/
    
copy or `scp` your `.env` file into the `app` root

.. code-block:: bash

    cp /some/path/to/.env ~/app/.env

    scp .production ambition@example.com:~/app/.env

edit `~/app/.env` file as required, for example

from `app/` build images for `ambition_production` and `mysql` and bring them `up`
    
.. code-block:: bash

    docker-compose -f compose/local.yml build \
    && docker-compose -f compose/local.yml up
    

.. note:: if you need to generate keys set ``DJANGO_AUTO_CREATE_KEYS=True`` in the ``.env``,
          ``docker-compose up``, change back to false and ``docker-compose up`` again.
          If needed, copy keys to container (e.g. you are using existing keys)

.. code-block:: bash

    docker cp /some/path/to/crypto_keys/ ambition_production:$DJANGO_KEY_FOLDER
    
Copy the `randomization_list.csv` file to the container

.. code-block:: bash

    docker cp /some/path/to/randomization_list.csv ambition_production:$DJANGO_ETC_FOLDER

In another shell, log into the container

.. code-block:: bash

    docker exec -it ambition_production /bin/bash

run migrations and other management commands as required
    
.. code-block:: bash

    python manage.py migrate
    python manage.py import_holidays
    python manage.py migrate import_randomization_list 

While still in the container, run check

.. code-block:: bash

    python manage.py check

Start runserver

.. code-block:: bash

    python manage.py runserver 0.0.0.0:8000
    



.. |pypi| image:: https://img.shields.io/pypi/v/ambition-edc.svg
    :target: https://pypi.python.org/pypi/ambition-edc
    
.. |travis| image:: https://travis-ci.com/ambition-trial/ambition-edc.svg?branch=develop
    :target: https://travis-ci.com/ambition-trial/ambition-edc
    
.. |coverage| image:: https://coveralls.io/repos/github/ambition-trial/ambition-edc/badge.svg?branch=develop
    :target: https://coveralls.io/github/ambition-trial/ambition-edc?branch=develop

.. _django-environ: https://github.com/joke2k/django-environ
.. _12-factor-django: http://www.wellfireinteractive.com/blog/easier-12-factor-django/
.. _env.sample: https://github.com/ambition-trial/ambition/blob/develop/env.sample
.. _Docker: https://docs.docker.com/compose/install/
