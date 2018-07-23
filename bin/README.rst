Ambition deployment
-------------------


Gunicorn
========

Copy the service files to ``systemd``

.. code-block:: bash

	$ sudo cp -R ~/ambition/bin/systemd/* /etc/systemd/system/

Create the sockets

.. code-block:: bash

	$ sudo systemctl start gunicorn-blantyre.socket \
	    && sudo systemctl start gunicorn-capetown.socket \
	    && sudo systemctl start gunicorn-gaborone.socket \
	    && sudo systemctl start gunicorn-harare.socket \
	    && sudo systemctl start gunicorn-kampala.socket \
	    && sudo systemctl start gunicorn-lilongwe.socket

If copying new files, you may be asked to run:

.. code-block:: bash

	sudo systemctl daemon-reload

Enable the sockets

.. code-block:: bash

	$ sudo systemctl enable gunicorn-blantyre.socket \
	    && sudo systemctl enable gunicorn-capetown.socket \
	    && sudo systemctl enable gunicorn-gaborone.socket \
	    && sudo systemctl enable gunicorn-harare.socket \
	    && sudo systemctl enable gunicorn-kampala.socket \
	    && sudo systemctl enable gunicorn-lilongwe.socket

``Output``

.. code-block:: bash

	Created symlink /etc/systemd/system/sockets.target.wants/gunicorn-blantyre.socket → /etc/systemd/system/gunicorn-blantyre.socket.
	Created symlink /etc/systemd/system/sockets.target.wants/gunicorn-capetown.socket → /etc/systemd/system/gunicorn-capetown.socket.
	Created symlink /etc/systemd/system/sockets.target.wants/gunicorn-gaborone.socket → /etc/systemd/system/gunicorn-gaborone.socket.
	Created symlink /etc/systemd/system/sockets.target.wants/gunicorn-harare.socket → /etc/systemd/system/gunicorn-harare.socket.
	Created symlink /etc/systemd/system/sockets.target.wants/gunicorn-kampala.socket → /etc/systemd/system/gunicorn-kampala.socket.
	Created symlink /etc/systemd/system/sockets.target.wants/gunicorn-lilongwe.socket → /etc/systemd/system/gunicorn-lilongwe.socket.


If you wish, you can check the status of each:

.. code-block:: bash

	$ sudo systemctl status gunicorn-blantyre
	$ sudo systemctl status gunicorn-capetown
	$ sudo systemctl status gunicorn-gaborone
	$ sudo systemctl status gunicorn-harare
	$ sudo systemctl status gunicorn-kampala
	$ sudo systemctl status gunicorn-lilongwe

``Output, inactive (first time)``


	● gunicorn-blantyre.service - gunicorn daemon
	   Loaded: loaded (/etc/systemd/system/gunicorn-blantyre.service; enabled; vendor preset: enabled)
	   Active: inactive (dead) since Mon 2018-07-23 17:57:25 UTC; 2min 56s ago
	 Main PID: 22953 (code=exited, status=0/SUCCESS)

Try accessing:

.. code-block:: bash

	curl --unix-socket /run/gunicorn-blantyre.sock localhost

``Output now shows active``

.. code-block:: bash

	● gunicorn-blantyre.service - gunicorn daemon
	   Loaded: loaded (/etc/systemd/system/gunicorn-blantyre.service; enabled; vendor preset: enabled)
	   Active: active (running) since Mon 2018-07-23 16:09:01 UTC; 14s ago
	 Main PID: 6839 (gunicorn)
	    Tasks: 4 (limit: 2361)
	   CGroup: /system.slice/gunicorn-blantyre.service
	           ├─6839 /home/ambition/.venvs/ambition/bin/python3 /home/ambition/.venvs/ambition/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ambition/
	           ├─6889 /home/ambition/.venvs/ambition/bin/python3 /home/ambition/.venvs/ambition/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ambition/
	           ├─6897 /home/ambition/.venvs/ambition/bin/python3 /home/ambition/.venvs/ambition/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ambition/
	           └─6908 /home/ambition/.venvs/ambition/bin/python3 /home/ambition/.venvs/ambition/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ambition/

	Jul 23 16:09:01 edc2 systemd[1]: Started gunicorn daemon.
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6839] [INFO] Starting gunicorn 19.9.0
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6839] [INFO] Listening at: unix:/home/ambition/ambition/gunicorn-blantyre.sock (6839)
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6839] [INFO] Using worker: sync
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6889] [INFO] Booting worker with pid: 6889
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6897] [INFO] Booting worker with pid: 6897
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6908] [INFO] Booting worker with pid: 6908


if there are any problems check:
	
.. code-block:: bash

	$ sudo journalctl -u gunicorn-blantyre   # etc

If the code base changes:

.. code-block:: bash

	$ sudo systemctl daemon-reload
	$ sudo systemctl restart gunicorn-blantyre \
  	    && sudo systemctl restart gunicorn-capetown \
	    && sudo systemctl restart gunicorn-gaborone \
	    && sudo systemctl restart gunicorn-harare \
	    && sudo systemctl restart gunicorn-kampala \
	    && sudo systemctl restart gunicorn-lilongwe

If needed, stop each service and start over ...

.. code-block:: bash

	$ sudo systemctl stop gunicorn-blantyre.socket \
  	    && sudo systemctl stop gunicorn-capetown.socket \
	    && sudo systemctl stop gunicorn-gaborone.socket \
	    && sudo systemctl stop gunicorn-harare.socket \
	    && sudo systemctl stop gunicorn-kampala.socket \
	    && sudo systemctl stop gunicorn-lilongwe.socket

	$ sudo systemctl stop gunicorn-blantyre \
  	    && sudo systemctl stop gunicorn-capetown \
	    && sudo systemctl stop gunicorn-gaborone \
	    && sudo systemctl stop gunicorn-harare \
	    && sudo systemctl stop gunicorn-kampala \
	    && sudo systemctl stop gunicorn-lilongwe \
	    && sudo systemctl daemon-reload


Nginx
=====

Copy the configurations to ``/etc/nginx/sites-available``

.. code-block:: bash

	$ sudo cp -R ~/ambition/bin/nginx/* /etc/nginx/sites-available/


Enable each site:

.. code-block:: bash

	$ sudo ln -s /etc/nginx/sites-available/blantyre.conf /etc/nginx/sites-enabled \
	    && sudo ln -s /etc/nginx/sites-available/capetown.conf /etc/nginx/sites-enabled \
	    && sudo ln -s /etc/nginx/sites-available/gaborone.conf /etc/nginx/sites-enabled \
	    && sudo ln -s /etc/nginx/sites-available/harare.conf /etc/nginx/sites-enabled \
	    && sudo ln -s /etc/nginx/sites-available/kampala.conf /etc/nginx/sites-enabled \
	    && sudo ln -s /etc/nginx/sites-available/lilongwe.conf /etc/nginx/sites-enabled


.. code-block:: bash

	$ sudo nginx -t

.. code-block:: bash

	$ sudo systemctl restart nginx

Firewall
========

Check ``ufw`` to open ``openSSH``, ``http``, ``https``, ``631``

Also check cloud firewall to ensure these ports are open


Certificates
============

The Nginx configurations make reference to certificates for the HTTPS redirect.

Generate certificates
+++++++++++++++++++++

If certificates do not exist, you can create then like this. 

Install certbot:

.. code-block:: bash

	$ sudo apt-get update
	$ sudo apt-get install software-properties-common
	$ sudo add-apt-repository ppa:certbot/certbot
	$ sudo apt-get update
	$ sudo apt-get install python-certbot-nginx 


then 

.. code-block:: bash

  sudo certbot certonly --manual --preferred-challenges=dns \
    --email=ew2789@gmail.com \
    --server=https://acme-v02.api.letsencrypt.org/directory \
    --agree-tos \
    -d clinicedc.org
    -d "*.clinicedc.org"

follow the instructions. You will need to update the dns TXT record.


Setup auto-renew
++++++++++++++++

TODO



