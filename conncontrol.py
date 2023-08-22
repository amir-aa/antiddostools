import os
from plyer import notification
ipdict={}
#Constants
CONNNUMBERTRIGGER=12
SYNRECVTRIGGER=10
CRITICALPORTS=[3389,21]
TRUSTEDIPS=[]
#-----------------------
def NotifGenerate():
    pass
def isdangerous(ip,remoteip:list,localport:int):
    connnumber=remoteip.count(ip)
    if(CONNNUMBERTRIGGER<connnumber):
        return True
    if(localport in CRITICALPORTS and remoteip not in TRUSTEDIPS):
        return True
    
def main():
    os.system('netstat -tna > %appdata%\etemp.txt ')
    PATH=os.getenv('APPDATA')+'\\etemp.txt'
    with open(PATH,'r+') as f:
        remoteaddr=[]
        conntype=[]
        lines=f.readlines()
        if len(lines)>1:
            for line in lines:
                splited=line.split()
                remoteaddr.append(splited[2])
                conntype.append(splited[3])
                if len(conntype)> SYNRECVTRIGGER:
                    NotifGenerate()
                localport=splited[1].split(':')[1]

def blockip(ip):
    os.system(f"netsh advfirewall firewall add rule name='Block {ip}' protocol=any dir=in enable=yes action=block profile=any remoteip={ip}")
