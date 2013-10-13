
#           opcode  operation
#             1     Read request (RRQ)
#             2     Write request (WRQ)
#             3     Data (DATA)
#             4     Acknowledgment (ACK)
#             5     Error (ERROR)

import socket, sys, struct, string, array

ErrorMsg = ['Not defined, see error message (if any).', 'File not found.', 'Access violation.', 'Disk full or allocation exceeded.' , 'Illegal TFTP Operation.', 'Illegal TFTP operation.', 'Unknown transfer ID.', 'File already exists.', 'No such user.', 'Failed to negotiate options']
ErrorCode = array.array('i');
host = sys.argv[1]
transfermode = sys.argv[2]
filename = sys.argv[3]
#UDP_PORT = sys.argv[4]

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
mode = "octet"

def main():
    if transfermode == "lesa":
        request(1, filename)
    elif transfermode == "skrifa":
        request(2, filename)
    else:
        print('Please use Servername Read/Write FileName')

def request (trmode, filenm):
    format = "!H%ds" % (len(filenm)+1)
    format += "%ds" % (len(mode)+1)
    s = struct.pack(format, trmode , filenm, mode)
    try:
        sock.sendto(s,(host,69))
        data, svar = sock.recvfrom(1024)
        port = svar[1]
        if trmode == 1:
            read(port, data)
        elif trmode == 2:
            write(port, data)
    except:
        print("Cannot connect to " + host)
        
def checkPackage(package):
    pack = struct.unpack("!HH", package[:4])
    if(pack[0] == 5):
        ErrorCode.insert(0, pack[0])
        ErrorCode.insert(1, pack[1])
        return False
    else:
        return True

def read(prt, dta):
    nextblock = 1
    strong = dta[4:]
    if checkPackage(dta) == False:
        print ErrorMsg[ErrorCode.index(1)]
        #Restart application and ask for new input
    else:
        if len(dta) == 516:
            Receiving = True;
        #While loop to recvieve all packages.
        while Receiving:
            #if last package was just received - sending last ACK pack.
            if len(dta) != 516:
                Receiving = False;
                ack = struct.pack("!HH", 4 , nextblock)
                sock.sendto(ack,(host,prt))
                writeToFile(strong)
            #receiving packages.
            else:
                ack = struct.pack("!HH", 4 , nextblock)
                sock.sendto(ack,(host,prt))
                dta, svar = sock.recvfrom(1024)
                strong += dta [4:]
                nextblock += 1  
            
def write(dta, prt):
    #TODO Implement
    print('Writing')

def writeToFile(strong):
    #CREATE FILE AND WRITE TO IT.
    fo = open(filename, "wb")
    fo.write(strong)
    #Closing open files and socket
    fo.close()
    sock.close()
    print('File Recieved')

if __name__ == "__main__":
    main()
   
