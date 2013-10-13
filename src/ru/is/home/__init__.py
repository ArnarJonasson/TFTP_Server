import socket
import sys
import struct
import string


Receiving = False;
#useless later Input1.  
UDP_IP = ""
#Given
UDP_PORT = 69

var = raw_input("Enter something: ")
#Input1 = servername
#Input2 = Read or Write
#Input3 = Document Name
input1,input2,input3 = var.split(" ")

if input2 == "lesa":
    UDP_IP = input1
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #sock.connect((UDP_IP, UDP_PORT))
    filename = input3
    mode = "octet"
    format = "!H%ds" % (len(filename)+1)
    format += "%ds" % (len(mode)+1)
    #packing read request
    s = struct.pack(format, 1, filename, mode)
    #sending read request
    sock.sendto(s,(UDP_IP,69))
    nextblock = 1
    lastpkt = s
    data, svar = sock.recvfrom(1024)
    strong = ""
    strong = data[4:]
    if len(data) == 516:
        Receiving = True;
    #While loop to recvieve all packages.
    while Receiving:
        #if last package was just received - sending last ACK pack.
        if len(data) != 516:
            Receiving = False;
            ack = struct.pack("!HH", 4 , nextblock)
            sock.sendto(ack,(UDP_IP,svar[1]))
        #receiving packages.
        else:
            ack = struct.pack("!HH", 4 , nextblock)
            sock.sendto(ack,(UDP_IP,svar[1]))
            data, svar = sock.recvfrom(1024)
            strong += data [4:]
            nextblock += 1
            
    #CREATE FILE AND WRITE TO IT.
    fo = open(filename, "wb")
    fo.write(strong)
    #Closing open files and socket
    fo.close()
    sock.close()
    print('File Recieved')
elif input2 == "skrifa":
    #implement Writing
    print('WRITING')
    
else:
    #ERROR EXPLAIN SYNTAX
    print('Please use Servername Read/Write FileName')