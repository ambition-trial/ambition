


.. code-block:: bash

	mkdir ~/tmp && cd ~/tmp && \
	curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

	sha256sum Miniconda3-latest-Linux-x86_64.sh

	sh Miniconda3-latest-Linux-x86_64.sh

	conda config --set auto_activate_base false

	conda init bash

Restart the shell

.. code-block:: bash

	~$ conda create -n edc python=3.7

	conda activate edc