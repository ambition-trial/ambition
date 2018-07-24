Ambition deployment
-------------------


Gunicorn
========

Copy the service files to ``systemd``

.. code-block:: bash

	$ sudo cp -R ~/app/bin/systemd/* /etc/systemd/system/

Create the sockets

.. code-block:: bash

	$ sudo systemctl start gunicorn.socket

If copying new files, you may be asked to run:

.. code-block:: bash

	$ sudo systemctl daemon-reload

Enable the sockets

.. code-block:: bash

	$ sudo systemctl enable gunicorn.socket

``Output``

.. code-block:: bash

	Created symlink /etc/systemd/system/sockets.target.wants/gunicorn.socket → /etc/systemd/system/gunicorn.socket.


If you wish, you can check the status of each:

.. code-block:: bash

	$ sudo systemctl status gunicorn

``Output, inactive (first time)``


	● gunicorn.service - gunicorn daemon
	   Loaded: loaded (/etc/systemd/system/gunicorn.service; enabled; vendor preset: enabled)
	   Active: inactive (dead) since Mon 2018-07-23 17:57:25 UTC; 2min 56s ago
	 Main PID: 22953 (code=exited, status=0/SUCCESS)

Try accessing:

.. code-block:: bash

	curl --unix-socket /run/gunicorn.sock localhost

``Output now shows active``

.. code-block:: bash

	● gunicorn.service - gunicorn daemon
	   Loaded: loaded (/etc/systemd/system/gunicorn.service; enabled; vendor preset: enabled)
	   Active: active (running) since Mon 2018-07-23 16:09:01 UTC; 14s ago
	 Main PID: 6839 (gunicorn)
	    Tasks: 4 (limit: 2361)
	   CGroup: /system.slice/gunicorn.service
	           ├─6839 /home/ambition/.venvs/ambition/bin/python3 /home/ambition/.venvs/ambition/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/
	           ├─6889 /home/ambition/.venvs/ambition/bin/python3 /home/ambition/.venvs/ambition/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/
	           ├─6897 /home/ambition/.venvs/ambition/bin/python3 /home/ambition/.venvs/ambition/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/
	           └─6908 /home/ambition/.venvs/ambition/bin/python3 /home/ambition/.venvs/ambition/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/

	Jul 23 16:09:01 edc2 systemd[1]: Started gunicorn daemon.
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6839] [INFO] Starting gunicorn 19.9.0
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6839] [INFO] Listening at: unix:/run/gunicorn.sock (6839)
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6839] [INFO] Using worker: sync
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6889] [INFO] Booting worker with pid: 6889
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6897] [INFO] Booting worker with pid: 6897
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6908] [INFO] Booting worker with pid: 6908


if there are any problems check:
	
.. code-block:: bash

	$ sudo journalctl -u gunicorn   # etc

If the code base changes:

.. code-block:: bash

	$ sudo systemctl daemon-reload
	$ sudo systemctl restart gunicorn

If needed to reset ...

.. code-block:: bash

	$ sudo systemctl stop gunicorn.socket &&
		&& sudo systemctl stop gunicorn \
		&& sudo systemctl disable gunicorn.socket

	$ sudo systemctl stop gunicorn-uat.socket &&
		&& sudo systemctl stop gunicorn-uat \
		&& sudo systemctl disable gunicorn-uat.socket


Nginx
=====

Copy the configurations to ``/etc/nginx/sites-available``

.. code-block:: bash

	$ sudo cp -R ~/app/bin/nginx/* /etc/nginx/sites-available/


Enable each site:

.. code-block:: bash

	$ sudo ln -s /etc/nginx/sites-available/ambition.conf /etc/nginx/sites-enabled


Disable the default site:

.. code-block:: bash
	
	$ sudo unlink /etc/nginx/sites-enabled/default

.. code-block:: bash

	$ sudo nginx -t

.. code-block:: bash

	$ sudo systemctl restart nginx

Firewall
========

Check ``ufw`` to open ``openSSH``, ``http``, ``https``, ``631``

Also check cloud firewall to ensure these ports are open


Certificates and HTTPS configuration
====================================

see  https://certbot.eff.org 


Configure droplet from base
---------------------------

Base droplet snapshot is ``ambgab``. Once the new droplet is created some config needs to be changed.

Update env
++++++++++

Log in as ``ambition``

Update the repo

	$ cd ~/app $ git pull

Check .env to update the following variables:

- DJANGO_ALLOWED_HOSTS
- DJANGO_CUPS_SERVERS
- DJANGO_LANGUAGES
- DJANGO_SITE_ID
- DJANGO_TIME_ZONE
- DJANGO_TOWN

Repeat the above for the ``uat`` account.


Update web services
+++++++++++++++++++

Log in as ``ambition``

These changes can be done from one account.

Reset the nginx configuration to listen on 80 only. certbot will add an HTTPS server block.

Unlink uat.conf

.. code-block:: bash

	$ sudo unlink /etc/nginx/sites-enabled/ambition.conf
	$ sudo unlink /etc/nginx/sites-enabled/uat.conf
	$ sudo unlink /etc/nginx/sites-enabled/ambition-uat.conf

Copy original ``conf`` files from the repo

.. code-block:: bash

	$ sudo cp -R ~/app/bin/nginx/* /etc/nginx/sites-available/

Update the ``server_name``:

.. code-block:: bash

	$ sudo nano /etc/nginx/sites-available/ambition.conf

	$ sudo nano /etc/nginx/sites-available/ambition-uat.conf


Enable each site:

.. code-block:: bash

	$ sudo ln -s /etc/nginx/sites-available/ambition.conf /etc/nginx/sites-enabled

	$ sudo ln -s /etc/nginx/sites-available/ambition-uat.conf /etc/nginx/sites-enabled


Get new certificates and configure for HTTPS:

.. code-block:: bash

	$ certbot --nginx


Apply to both sites and selected to redirect all traffic to HTTPS.

Check the files
	
.. code-block:: bash

	$ sudo nginx -t


Restart nginx

.. code-block:: bash

	$ sudo systemctl restart nginx
