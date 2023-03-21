import os 
import json 
class Dumps:
    def __init__(self,km):
        self.files = []

        self.list_files(km)
    
    def list_files(self,km):
        for f in os.listdir(str(km)+"km"):
            if '.csv' in f:
                print("removing ",f)
                os.remove(str(km)+"km/"+f)
            if '.json' in f:
                self.files.append(str(km)+"km/"+f)
    
    def start(self):
        #print(self.files)
        for f in self.files:
            outfile = f.replace(".json",".csv")
            print(f, outfile)
            self.read(f,outfile)

    def read(self, path, outfile):
        o = open(path,"r")    
        line = o.readline()
        while line:
            #print(line)
            line = line.strip()
            obj = eval(line)

            rlen = None 
            dl = None 

            msg = ""
            if 't_start' in obj:
                msg=msg+str(obj['t_start'])+","
            if 't_stop' in obj:
                msg=msg+str(obj['t_stop'])+","
            if 'delay' in obj:
                msg=msg+str(obj['delay'])+","
                dl = int(obj['delay'])
            if 'tries' in obj:
                msg=msg+str(obj['tries'])+","
            if 'memfree' in obj:
                msg=msg+str(obj['memfree'])+","
            if 'frag_count' in obj:
                msg=msg+str(obj['frag_count'])+","
            if 'received_len' in obj:
                msg=msg+str(obj['received_len'])+","
                rlen = int(obj['received_len'])
            if  'hall' in obj:
                msg=msg+str(obj['hall'])+","
            if 'temp' in obj:
                msg=msg+str(obj['temp'])+","
            if rlen and dl:
                bw = ((rlen*8)/((dl/2)/1000))/1024
                msg+="{:.2f}".format(bw)+","

            msg = msg[:-1]
            #msg = ','.join(map(str,[obj['t_start'],obj['t_stop'],obj['delay'], obj['tries'],obj['memfree']]))

            #print(msg)
            self.write(outfile,msg)
            line = o.readline()
        o.close()
    def write(self,path,msg):
        w = open(path,"a")
        w.write(msg+"\n")
        w.close()

if __name__ == "__main__":
    for i in range(1,6):
        print(i)
        d = Dumps(i)
        d.start()