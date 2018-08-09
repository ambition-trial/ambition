
Installation
++++++++++++


Install CUPS Print Server::

	sudo apt-get install 

	sudo cp /etc/cups/cupsd.conf /etc/cups/cupsd.conf.original
	
	sudo chmod a-w /etc/cups/cupsd.conf.original

Edit ``/etc/cups/cupsd.conf`` to listin on the public IP::

	sudo  nano /etc/cups/cupsd.conf

Add the last line with your public IP::

	    Listen 127.0.0.1:631           # existing loopback Listen
	    Listen /var/run/cups/cups.sock # existing socket Listen
	--> Listen PUBLIC_IP:631      # Listen on the LAN interface, Port 631 (IPP)

Restart CUPS::

	sudo systemctl restart cups.service

Add a remote printer
++++++++++++++++++++

``LOCAL_PRINTER_NAME``: printer as named on the EDC, your server

``REMOTE_IP_ADDRESS``: IP of remote CUPS server

``PRINTER_NAME``: printer name installed on remote CUPS server

For example::

	lpadmin -p LOCAL_PRINTER_NAME -E -v ipp://REMOTE_IP_ADDRESS/printers/PRINTER_NAME

