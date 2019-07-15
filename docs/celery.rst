

.. code-block:: bash

	$ sudo rabbitmqctl add_user myuser mypassword

	$ sudo rabbitmqctl add_vhost myvhost
	
	$ sudo rabbitmqctl set_user_tags myuser mytag
	
	$ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"



Settings
++++++++

Add the following to settings.py. When ready, set ``CELERY_ENABLED`` = True.

.. code-block:: bash

	# settings.py

	...

	# CELERY STUFF
	CELERY_BROKER_USER=<user>
	CELERY_BROKER_PASSWORD=<password>
	CELERY_BROKER_HOST=<mq host>
	CELERY_BROKER_PORT=5672
	CELERY_ENABLED=False

	...


Usage systemd
+++++++++++++

See http://docs.celeryproject.org/en/latest/userguide/daemonizing.html#usage-systemd

adduser celery

