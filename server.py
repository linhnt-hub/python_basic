#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Thinkpad E570
#
# Created:     15/11/2019
# Copyright:   (c) Thinkpad E570 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import socket
T_PORT = 8080
TCP_IP = '127.0.0.1'
BUF_SIZE = 1024
# create a socket object name 'k'
k = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
k.bind((TCP_IP, T_PORT))
k.listen(1)
con, addr = k.accept()
print ('Connection Address is: ' , addr)
while True :
    data = con.recv(BUF_SIZE) 
    if not data:break
    
print ("Received data", data)
con.send(data.encode())
con.close()
