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
transfermode = sys.argv[2].lower()
filename = sys.argv[3]
if(len(sys.argv)==5):
    UDP_PORT = int(sys.argv[4]);
else: UDP_PORT = 69;

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
mode = "octet"

def main():
    if transfermode == "lesa":
        request(1, filename, host)
    elif transfermode == "skrifa":
        try:
            fo = open(filename, "r")
            str = fo.read()
        except:
            print("File Not Found")
            str = None
        if str == None:
            print("Error in Opening File")
        else:
            request(2, filename, host)
    else:
        print('Please use Servername Read/Write FileName')
        
def request (trmode, filenm, Host):
    if Host[0].isalpha():
        try:
            Host = socket.gethostbyname(Host)
        except:
            print("Cannot get host by name")
    format = "!H%ds" % (len(filenm)+1)
    format += "%ds" % (len(mode)+1)

    s = struct.pack(format, trmode , filenm, mode)
    sock.settimeout(5)
    try:
        sock.sendto(s,(Host,UDP_PORT))
        data, svar = sock.recvfrom(1024)
        port = svar[1]
        if trmode == 1:
            read(port, data, Host)
        elif trmode == 2:
            write(port, data, Host)
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

def read(prt, dta, Host):
    nextblock = 1
    strong = dta[4:]
    if checkPackage(dta) == False:
        print ErrorMsg[ErrorCode.index(1)]
        #Restart application and ask for new input
    else:
        Receiving = True;
        #While loop to recvieve all packages.   
        while Receiving:
            #if last package was just received - sending last ACK pack.
            if len(dta) != 516:
                Receiving = False;
                ack = struct.pack("!HH", 4 , nextblock)
                sock.sendto(ack,(Host,prt))
                writeToFile(strong)
            #receiving packages.
            else:
                ack = struct.pack("!HH", 4 , nextblock)
                sock.sendto(ack,(Host,prt))
                dta, svar = sock.recvfrom(1024)
                strong += dta [4:]
                nextblock += 1          
                
def getdata():
    try:
        fo = open(filename, "r")
        str = fo.read()
    except:
        str = None
    return str
        
            
def write(prt, dta, Host):
    #currentblock we're sending
    nextblock = 1
    #current letter to send
    currentlet = 0
    #Max length to add to packages
    packmax = 512
    #DAT format
    format = "!HH%ds" % 512
    #load up the data to send
    filedata = getdata()
    if filedata is None:
        print("Error in opening File")
    else:
        Sending = True
        while Sending:
            #send last package
            if packmax > len(filedata):
                #last package needs new format
                formatlastpack = "!HH%ds" % (len(filedata)-currentlet)
                Sending = False;
                #sending last package
                ack = struct.pack(formatlastpack, 3, nextblock, filedata[currentlet:len(filedata)])
                sock.sendto(ack,(Host,prt))
            #send other package
            else:
                #sending package number X
                ack = struct.pack(format, 3, nextblock, filedata[currentlet:packmax])
                sock.sendto(ack,(Host,prt))
                dta, svar = sock.recvfrom(1024)
                #Updating variables so we know where we are in the file
                currentlet = packmax+1
                packmax += 512+1
                nextblock += 1
            
        #TODO Implement
        print('Finished Writing')

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
