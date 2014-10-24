#!/usr/bin/env python
#===============================================================================
#
#          FILE:  portLocker.py
#         USAGE:  python portLocker.py
#   DESCRIPTION:  port blocker/unblocker via dropbox file
#        AUTHOR:  http://bynario.com
#       CREATED:  05/08/2014 17:37:23 CEST
#===============================================================================
import time,sys,os,subprocess

dbFile="https://www.dropbox.com/s/XXXXXXXXXXXXXXXX/file"
logFile="/var/log/locker_log.log"
htmlFile="/usr/share/nginx/www/sshd.html"
servicesL={'ssh':'22','vpn':'1723','httpd':'80'}
actionsL=('open','close')

def createWWW(filename):
    try:
        with open(filename, 'w') as f: f.write(getTime())
    except Exception as e:
        print2Log(logFile,"Error opening "+filename+": "+str(e))

def print2Log(filename,text):
    try:
        with open(filename, 'w') as f:
            f.write(getTime() + " - " + text+"\n")
    except Exception as e:
        print2Log(logFile,"Error opening "+filename+": "+str(e))

def print2WWW(filename,service,status):
    try:
        with open(filename, 'a') as f:
            f.write(" - Service: " + service + " - Status: " + status)
    except Exception as e:
        print2Log(logFile,"Error opening "+filename+": "+str(e))

def getTime():
    return time.strftime("%Y-%m-%d %H:%M")

def runCommand(command,retVal=None):
    try:
        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
        (output, err) = p.communicate()
        if retVal: return output
        else: return None
    except Exception as e:
        print2Log(logFile,"Error executing "+str(command)+": "+str(e))

def checkDBFile():
    action="/usr/bin/curl -s -L " + dbFile
    command=runCommand(action,retVal=True)
    return command

def runIptables(service,action):
    print getTime() + " Running iptables... Service: " + service + " Action:" + action
    check_command="/sbin/iptables -C INPUT -p tcp -m tcp --dport " + servicesL[service] +" -j DROP"
    try:
        check_output = subprocess.check_call(check_command.split(),stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        if action == "close": command="/sbin/iptables -A INPUT -p tcp --dport " + servicesL[service] + " -j DROP"
        else: return
    else:
        if action == "open": command="/sbin/iptables -D INPUT -p tcp --dport " + servicesL[service] + " -j DROP"
        else: return

    runCommand(command)

if __name__ == "__main__":
    createWWW(htmlFile)

    for line in checkDBFile().splitlines():
        if not line: continue
        if len(line.split()) != 2:
            print2Log(logFile,"Error in dropbox file: wrong format")
            sys.exit(1)
        else:
            act = line.split()[0]
            serv = line.split()[1]

            if servicesL.has_key(serv) and act in actionsL:
                runIptables(serv,act)
                print2WWW(htmlFile,serv,act)
            else:
                print
                print2Log(logFile,"Service or Action found in file not valid... Skipping: " + act + "-" + serv)
