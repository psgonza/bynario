#/usr/bin/env python2.7
"""
psgonza - 15-Oct-2016
Just a quick saturday morning hack:
- Whatever file in magicBoxPath will be encrypted using GPG and moved to dropbox_private_folder with the ".gpg" extension
- Whatever file in magicBoxPath with the ".gpg" extension will be decrypted and moved to local_private_folder
Todo:
- GPG Key management
- Directory support
- Improve pooling (watchdog?)
"""
import sys,os
import datetime
from time import sleep
from datetime import datetime

try:
    import gnupg
except ImportError as e:
    print("Module gnupg not found")
    sys.exit(1)     

#Files and Folders
dropbox_private_folder = '/home/test/dropbox'
local_private_folder = '/home/test/dropbox_local'
magicBoxPath = '/home/test/temporary_path'
gngpghomePath = '/home/test/gpghome'
logFile = 'gpg2dropbox.log'

#GNUPG variables
gnuPassphrase = 'password'
gnupgMail = 'test@test.com'

def initGPG():
    #Initialize the GPG object
    try:
        gpgobj = gnupg.GPG(gnupghome=gngpghomePath)
        logger('Starting %s'% sys.argv[0])
    except Exception as e:
        logger('Error starting %s: ' % (sys.argv[0], str(e)))
        sys.exit(1)
       
    return(gpgobj)

def watchDir():
    for files in os.listdir(magicBoxPath):
        if files.endswith('.gpg'): 
            decrypt_file(files)
        else:
            encrypt_file(files)
        
def logger(text):
    with open(logFile,'a') as fd:
        ts = datetime.strftime(datetime.now(),"%Y%m%d-%H%M%S")
        fd.write('* %s: %s\n' % (ts,text))

def encrypt_file(filename):
    srcFile = '%s/%s' % (magicBoxPath,filename) 
    dstFile = '%s/%s.gpg' % (dropbox_private_folder,filename) 
    try:
        with open(srcFile, 'rb') as f:
            status = gpg.encrypt_file(f, recipients=[gnupgMail],output=dstFile)
        if status.ok:
            removeFile(srcFile)    
        else:
            logger('\n'.join(status.ok,status.status,status.stderr))
    except Exception as e:
        logger(str(e))

def decrypt_file(filename):
    srcFile = '%s/%s' % (magicBoxPath,filename) 
    dstFile = '%s/%s' % (local_private_folder,filename[:-4])
    try:
        with open(srcFile, 'rb') as f:
            status = gpg.encrypt_file(f, recipients=[gnupgMail],output=dstFile)
        if status.ok:
            removeFile(srcFile)    
        else:
            logger('\n'.join(status.ok,status.status,status.stderr))
    except Exception as e:
        logger(str(e))
    
def removeFile(filename):
    try:
        os.unlink(filename)
    except:
        logger('Error removing %s')

if __name__ == "__main__":
    
    gpg = initGPG()
      
    while True:
        watchDir()
        try:
            sleep(30)
        except KeyboardInterrupt:
            break
    
    logger('%s stopped' % sys.argv[0])
    sys.exit(0)
