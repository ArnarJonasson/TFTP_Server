import socket
import sys
import struct
import string
        
#useless later Input1.  
UDP_IP = "127.0.0.1"
#Given
UDP_PORT = 69

var = input("Enter something: ")
#Input1 = servername
#Input2 = Read or Write
#Input3 = Document Name
input1,input2,input3 = var.split(" ")

if input2 == "lesa":
    #implement Reading
    print('READING')
elif input2 == "skrifa":
    #implement Writing
    print('WRITING')
    
else:
    #ATM only for connecting
    sock = socket.socket(socket.AF_INET,
                        socket.SOCK_DGRAM)
    s = struct.pack("!H", 4)
    sock.sendto(s,(UDP_IP,UDP_PORT))
    sock.close()