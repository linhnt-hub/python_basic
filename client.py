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

MSG = "Hello Linh"

# create a socket object name 'k'

k = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

k.connect((TCP_IP, T_PORT))

k.send(MSG.encode())

data = k.recv(BUF_SIZE)

k.close