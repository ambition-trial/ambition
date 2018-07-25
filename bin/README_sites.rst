
Setting up the project home page
--------------------------------


.. code-block:: bash

	$ sudo wget https://github.com/ambition-trial/ambition/blob/develop/bin/nginx/index.html /var/www/html

	$ sudo wget https://github.com/ambition-trial/ambition/blob/develop/bin/nginx/ambition-sites.conf /etc/nginx/sites-available

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