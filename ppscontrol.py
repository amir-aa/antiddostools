import psutil,time,threading
from pyfiglet import Figlet
import datetime
import sys
f = Figlet()
print (f.renderText('DDOS Identifier'))
overaldic={}
class NIC(threading.Thread):
    def __init__(self,name:str,nic:str,LogAll:bool=False,Threshold:int=800000): #for 10G NIC MAX 14000000pps 
        threading.Thread.__init__(self)
        self.nicname=name
        self.Threshold=Threshold
        self.nic=nic
        self.LogAll=LogAll
        

    def getpackets(self):
        datacollector = psutil.net_io_counters(pernic=True, nowrap=True)[self.nicname]
        return datacollector
        
    def Writelog(self,content:str):
        with open('ppscontrol.log','a')as f:
            f.write(content+'\n')
    def run(self):

        while True:
            rx=self.getpackets().packets_recv
            if rx !=0:
                pps=self.nicname,self.getpackets().packets_recv
                
                if self.LogAll:
                    self.Writelog(f"[x] {datetime.datetime.now()} ::Packets Per Second on {self.nicname} ::{pps[1]}!")
                elif int(pps[1]) > self.Threshold:
                    self.Writelog(f"{datetime.datetime.now()} ::Packets Per Second on {self.nicname} ::{pps[1]}!")
                overaldic[self.nicname]+=pps[1]
               
                time.sleep(5)
def CheckMAXpps(count:int=0,timecycle:int=10):
    """this function compares pps per NIC sorted in dictionary, 5 times every 10 seconds by default|count=0 means endless """

    i=1
    while True:
        time.sleep(timecycle)
        print(overaldic)
        print({k: v for k, v in sorted(overaldic.items(), key=lambda item: item[1],reverse=True)})#sorting
        i+=1
        if(i==count):
            break


           
                
if __name__=="__main__":
    
    tbox=[]
    for nic in psutil.net_if_stats():
        overaldic[nic]=0 #set 0 for all nic(s) to calculate overal recieved packets 
        tbox.append(NIC(nic,nic,False))
    threading.Thread(target=CheckMAXpps).start()
    for i in tbox:
        i.start()
        #print("Thread Started")
