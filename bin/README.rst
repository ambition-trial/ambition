Ambition deployment
-------------------


Gunicorn
========

Copy the service files to ``systemd``

.. code-block:: bash

	$ sudo cp -R ~/ambition/bin/systemd/* /etc/systemd/system/

Start each service

.. code-block:: bash

	$ sudo systemctl start gunicorn.blantyre \
  	    && sudo systemctl start gunicorn.capetown \
	    && sudo systemctl start gunicorn.gaborone \
	    && sudo systemctl start gunicorn.harare \
	    && sudo systemctl start gunicorn.kampala \
	    && sudo systemctl start gunicorn.lilongwe

``No output unless you are copying over existing services``

.. code-block:: bash

	Warning: The unit file, source configuration file or drop-ins of gunicorn.blantyre.service changed on disk. Run 'systemctl daemon-reload' to reload units.
	Warning: The unit file, source configuration file or drop-ins of gunicorn.capetown.service changed on disk. Run 'systemctl daemon-reload' to reload units.
	Warning: The unit file, source configuration file or drop-ins of gunicorn.gaborone.service changed on disk. Run 'systemctl daemon-reload' to reload units.
	Warning: The unit file, source configuration file or drop-ins of gunicorn.harare.service changed on disk. Run 'systemctl daemon-reload' to reload units.
	Warning: The unit file, source configuration file or drop-ins of gunicorn.kampala.service changed on disk. Run 'systemctl daemon-reload' to reload units.
	Warning: The unit file, source configuration file or drop-ins of gunicorn.lilongwe.service changed on disk. Run 'systemctl daemon-reload' to reload units.

if so, run:

.. code-block:: bash

	$ sudo systemctl daemon-reload

Enable each service

.. code-block:: bash

	$ sudo systemctl enable gunicorn.blantyre \
	    && sudo systemctl enable gunicorn.capetown \
	    && sudo systemctl enable gunicorn.gaborone \
	    && sudo systemctl enable gunicorn.harare \
	    && sudo systemctl enable gunicorn.kampala \
	    && sudo systemctl enable gunicorn.lilongwe

``Output, if done for the first time.``

.. code-block:: bash

	Created symlink /etc/systemd/system/multi-user.target.wants/gunicorn.blantyre.service → /etc/systemd/system/gunicorn.blantyre.service.
	Created symlink /etc/systemd/system/multi-user.target.wants/gunicorn.capetown.service → /etc/systemd/system/gunicorn.capetown.service.
	Created symlink /etc/systemd/system/multi-user.target.wants/gunicorn.gaborone.service → /etc/systemd/system/gunicorn.gaborone.service.
	Created symlink /etc/systemd/system/multi-user.target.wants/gunicorn.harare.service → /etc/systemd/system/gunicorn.harare.service.
	Created symlink /etc/systemd/system/multi-user.target.wants/gunicorn.kampala.service → /etc/systemd/system/gunicorn.kampala.service.
	Created symlink /etc/systemd/system/multi-user.target.wants/gunicorn.lilongwe.service → /etc/systemd/system/gunicorn.lilongwe.service.


If you wish, you can check the status of each:

.. code-block:: bash

	$ sudo systemctl status gunicorn.blantyre
	$ sudo systemctl status gunicorn.capetown
	$ sudo systemctl status gunicorn.gaborone
	$ sudo systemctl status gunicorn.harare
	$ sudo systemctl status gunicorn.kampala
	$ sudo systemctl status gunicorn.lilongwe

``Output, for each should be something like this``


.. code-block:: bash

	● gunicorn.blantyre.service - gunicorn daemon
	   Loaded: loaded (/etc/systemd/system/gunicorn.blantyre.service; enabled; vendor preset: enabled)
	   Active: active (running) since Mon 2018-07-23 16:09:01 UTC; 14s ago
	 Main PID: 6839 (gunicorn)
	    Tasks: 4 (limit: 2361)
	   CGroup: /system.slice/gunicorn.blantyre.service
	           ├─6839 /home/ambition/.venvs/ambition/bin/python3 /home/ambition/.venvs/ambition/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ambition/
	           ├─6889 /home/ambition/.venvs/ambition/bin/python3 /home/ambition/.venvs/ambition/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ambition/
	           ├─6897 /home/ambition/.venvs/ambition/bin/python3 /home/ambition/.venvs/ambition/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ambition/
	           └─6908 /home/ambition/.venvs/ambition/bin/python3 /home/ambition/.venvs/ambition/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ambition/

	Jul 23 16:09:01 edc2 systemd[1]: Started gunicorn daemon.
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6839] [INFO] Starting gunicorn 19.9.0
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6839] [INFO] Listening at: unix:/home/ambition/ambition/gunicorn.blantyre.sock (6839)
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6839] [INFO] Using worker: sync
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6889] [INFO] Booting worker with pid: 6889
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6897] [INFO] Booting worker with pid: 6897
	Jul 23 16:09:03 edc2 gunicorn[6839]: [2018-07-23 16:09:03 +0000] [6908] [INFO] Booting worker with pid: 6908


if there are any problems check:
	
.. code-block:: bash

	$ sudo journalctl -u gunicorn.blantyre   # etc

If the code base changes:

.. code-block:: bash

	$ sudo systemctl restart gunicorn
	$ sudo systemctl daemon-reload

If needed, stop each service

.. code-block:: bash

	$ sudo systemctl stop gunicorn.blantyre \
  	    && sudo systemctl stop gunicorn.capetown \
	    && sudo systemctl stop gunicorn.gaborone \
	    && sudo systemctl stop gunicorn.harare \
	    && sudo systemctl stop gunicorn.kampala \
	    && sudo systemctl stop gunicorn.lilongwe \
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
    -d *.clinicedc.org

follow the instructions. You will need to update the dns TXT record.


Setup auto-renew
++++++++++++++++

TODO



