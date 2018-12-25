

.. code-block:: bash

	$ sudo rabbitmqctl add_user myuser mypassword

	$ sudo rabbitmqctl add_vhost myvhost
	
	$ sudo rabbitmqctl set_user_tags myuser mytag
	
	$ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"




# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
