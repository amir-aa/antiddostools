import psutil,time
import datetime
CHECKCYCLE=5 #Check every %CHECKCYCLE% (seconds)
THRESHOLD=800000#log Threshold
def getpackets():
        datacollector = psutil.net_io_counters(pernic=True, nowrap=True)

        return datacollector
def Writelog(content:str):
        with open('ppscontrol.log','a')as f:
            f.write(content+'\n')
def main(buffer)->dict:
                
        

        result={}
        for nic in psutil.net_if_stats():
                rx=getpackets()[nic].packets_recv
                if rx!=0:
                        pps=(rx-buffer[nic].packets_recv)//CHECKCYCLE
                        result[nic]=pps

                        if(pps)>THRESHOLD:
                                Writelog(content=f"[x] {datetime.datetime.now()} ::Packets Per Second on {nic} ::{pps}!")
        return result

if __name__=='__main__':
        buffer=getpackets()
        while 1:
                
                
                print(datetime.datetime.now(),{k: v for k, v in sorted(main(buffer).items(), key=lambda item: item[1],reverse=True)})#sorting
                buffer=getpackets()
                time.sleep(CHECKCYCLE)

                
