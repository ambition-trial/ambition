
Setting up the project home page
--------------------------------


Clone the repo, if required:

.. code-block:: bash

	$ git clone https://github.com/ambition-trial/ambition.git

.. code-block:: bash

	$ sudo cp ambition/bin/nginx/index.html /var/www/html

	$ sudo cp ambition/bin/nginx/ambition-sites.conf /etc/nginx/sites-available/ambition-sites.conf

(if no longer required, delete the repo)

Unlink default

.. code-block:: bash

	$ sudo unlink /etc/nginx/sites-enabled/default

Enable ``ambition-sites``:

.. code-block:: bash

	$ sudo ln -s /etc/nginx/sites-available/ambition-sites.conf /etc/nginx/sites-enabled

Test and reload

.. code-block:: bash

	$ sudo nginx -t

	$ sudo systemctl restart nginx

Check

.. code-block:: bash

	$ curl http://ambition.clinicedc.org
