

sudo apt-get update

Basic local/development
------------------------
deploy using runserver (DEBUG=True)


# ENV copy to a file, edit, source

On your new droplet log in a root and create a new file ``env_setup`` with these variables.
Fill in the correct password for ``MYSQL_USER_PASSWORD``

.. code-block:: bash

	export APP_HOST=gaborone.uat.ambition.clinicedc.org
	export APP_NAME=ambition
	export APP_USER=ambition
	export APP_FOLDER=app
	export DJANGO_EXPORT_FOLDER=/home/$APP_USER/export
	export DJANGO_ETC_FOLDER=/home/$APP_USER/.etc/$APP_NAME
	export DJANGO_KEY_FOLDER=$DJANGO_ETC_FOLDER/crypto_fields
	export DJANGO_LOG_FOLDER=/home/$APP_USER/log
	export DJANGO_STATIC_FOLDER=/home/$APP_USER/static
	export MYSQL_DATABASE=ambition
	export MYSQL_USER=edc
	export MYSQL_USER_PASSWORD=password  # need a password
	export REPO=https://github.com/ambition-trial/ambition.git $APP_FOLDER
	export VENV=ambition


Source the file ``env_setup``.

.. code-block:: bash
	
	$ source env_setup
	$ echo $APP_FOLDER
	
	#output 
	app

As root, create the non-root account and setup keys for key-based authentication:

.. code-block:: bash

	# as root, create a non-root account and set up keys
	adduser $APP_USER
	# add to sudo
	usermod -aG sudo $APP_USER
	# copy keys to the new account
	mkdir /home/$APP_USER/.ssh
	cp .ssh/authorized_keys /home/$APP_USER/.ssh
	chown $APP_USER:$APP_USER -R /home/$APP_USER/.ssh
	chmod 700 /home/$APP_USER/.ssh
	chmod 600 /home/$APP_USER/.ssh/authorized_keys


Login as non-root account ``ambition`` and install dependencies.

.. code-block:: bash

	sudo apt-get update
	sudo apt-get -y upgrade
	sudo apt-get -y install mysql-server-5.7 # if needed
	sudo apt-get -y install mysql-client-5.7 libmysqlclient-dev libcups2-dev ipython3 python3-pip python3-dev python3-venv python3-cups python3-venv redis-server nginx curl


Reference
---------

Deploy onto an Ubuntu 18.04 server

* https://www.digitalocean.com/community/tutorials/systemd-essentials-working-with-services-units-and-the-journal
* https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-1604
* https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04
* https://github.com/joke2k/django-environ/blob/develop/README.rst
* https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04
* https://www.digitalocean.com/community/tutorials/how-to-set-up-object-storage-with-django
* https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04
* https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04
* https://certbot.eff.org/docs/install.html#docker-user
* https://certbot-dns-digitalocean.readthedocs.io/en/latest/
* https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-18-04
* https://realpython.com/caching-in-django-with-redis/
* https://realpython.com/caching-in-django-with-redis/
* https://niwinz.github.io/django-redis/latest/
* https://micropyramid.com/blog/how-to-monitor-django-application-live-events-with-sentry/
* https://docs.sentry.io/clients/python/integrations/django/

Misc

* https://www.digitalocean.com/community/tutorials/how-to-use-sshfs-to-mount-remote-file-systems-over-ssh
* https://www.digitalocean.com/community/tutorials/how-to-configure-custom-connection-options-for-your-ssh-client

