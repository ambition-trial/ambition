Configure droplet from base
---------------------------

Base droplet snapshot is ``ambgab``. Once the new droplet is created some config needs to be changed.

Update env
++++++++++

Log in as ``ambition``

Update the repo

.. code-block:: bash

  $ cd ~/app $ git pull

Check ``.env`` to update the following variables:

- DJANGO_ALLOWED_HOSTS
- DJANGO_CUPS_SERVERS
- DJANGO_LANGUAGES
- DJANGO_SITE_ID
- DJANGO_TIME_ZONE
- DJANGO_TOWN

**Repeat** the above for the ``uat`` account.

Update web services
+++++++++++++++++++

These changes can be done from one account.

Log in as ``ambition``

Reset the nginx configuration to listen on 80 only. certbot will add an HTTPS server block.

Unlink ``uat.conf``

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


Enable each available site:

.. code-block:: bash

  $ sudo ln -s /etc/nginx/sites-available/ambition.conf /etc/nginx/sites-enabled  
  $ sudo ln -s /etc/nginx/sites-available/ambition-uat.conf /etc/nginx/sites-enabled


Get new certificates and configure for HTTPS:

.. code-block:: bash

  $ certbot --nginx


Configure for both ``xxx.ambition.clinicedc.org`` and xxx.uat.ambition.clinicedc.org``and selected to redirect all traffic to HTTPS.

Check the files
  
.. code-block:: bash

  $ sudo nginx -t

Restart nginx

.. code-block:: bash

  $ sudo systemctl restart nginx

