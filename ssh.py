#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Thinkpad E570
#
# Created:     13/11/2019
# Copyright:   (c) Thinkpad E570 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#!/usr/bin/python           # This is server.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print ('Got connection from', addr)
   c.send('Thank you for connecting')
   c.close()                # Close the connection