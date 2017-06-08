import httplib,httplib,sys
import socket, re, ssl
from multiprocessing import Pool
from time import ctime

def Worker(CheckLatest,IP,Port):
    try:    
        CheckLatest.request("GET", "/")
        Response = CheckLatest.getresponse()
        Data = Response.read()
        if Port == 80:
            print "http://"+IP
        else:
            print "https://"+IP
        #print "\033[92m[+]\x1B[m %s:%s \x1B[m" % (IP, Port)
        try:
            title = re.findall(r'<title>(.*?)</title>',str(Data))[0]
        except IndexError:
            title = ""
        except httplib.BadStatusLine:
            pass
    except: 
        pass

def HTTPS(IP):
    try:
        IP = IP.rstrip()
        CheckLatest = httplib.HTTPSConnection(IP, timeout=5, port=443)
        Worker(CheckLatest, IP, 443)
    except ssl.CertificateError:
        HTTP(IP)
    except ssl.SSLError:
        HTTP(IP)
    except socket.error:
        HTTP(IP)
    except httplib.BadStatusLine:
        HTTP(IP)
    except socket.gaierror:
        pass

def HTTP(IP):
    try:
        IP = IP.rstrip()
        CheckLatest = httplib.HTTPConnection(IP, timeout=5, port=80)
        Worker(CheckLatest, IP, 80)
    except socket.gaierror:
        pass
    except socket.error: 
        pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "\033[91m[-]\x1B[m Usage: %s  <Domain List>" % sys.argv[0]
        sys.exit(1)

    else:
        filename = sys.argv[1]
        openafile = open(filename, 'r')
        readafile = openafile.readlines()

        try:
            count = len(readafile)
            if count > 500:
                print("\033[94m[*]\x1B[m Loading Please Wait")
            pool = Pool(100)
            pool.map(HTTPS, readafile)
            pool.close()
            pool.join()
            openafile.close()

        except KeyboardInterrupt:
            print("\033[94m[-]\x1B[m User Aborted Exiting")
            sys.exit(0)

        except IndexError:
            print ("This is not good")
            pass
