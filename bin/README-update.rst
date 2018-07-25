
Log in to the server as ``ambition``

.. code-block:: bash

	$ cd app && git pull

	$ sudo systemctl daemon-reload \
	  && sudo systemctl restart gunicorn

Switch to the ``uat`` user and repeat.
