import serial
import requests


todayStr = ""
tomorrowStr=""
e = "\xff\xff\xff"
myUrl = "https://script.google.com/macros/s/AKfycbwY2YIhEJeJc3GbmubJ4diF-R8mYYCfEiHH49LnxS70AvGRPskt/exec"

def getCal(url):
    global todayStr
    global tomorrowStr
    try:
        resp = requests.get(url)
    except:
        return ("REQUEST ERROR")
        exit
    #print("Response: "  + str(resp.status_code))
    if resp.status_code==200:
        #print(resp.content)
        root = resp.json()
        todayStr = " Today"
        for i in range(10):
                try:
                        ttitle = root["eventsToday"][i]["title"]
                except:
                        break
                ttime = root["eventsToday"][i]["time"]
                tevent = str("\\r  ") + ttitle + str(" ") + ttime
                todayStr += tevent;
    
        #print(todayStr)

        tomorrowStr = " Tomorrow";
        for j in range(10):
                try:
                        mtitle = root["eventsTomro"][j]["title"]
                except:
                        break
                mtime = root["eventsTomro"][j]["time"]
                mevent = str("\\r  ") + mtitle + str(" ") + mtime
                tomorrowStr += mevent
    
        #print(tomorrowStr)
        return("OK")
    else:
        return("INCORRECT STATUS CODE")

ser = serial.Serial(
        port = '/dev/ttyAMA0',
        baudrate = 9600,
        stopbits = serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=5)

if serial.VERSION <= "3.0":
    if not ser.isOpen():
        ser.open()
else:
    if not ser.is_open:
        ser.open()
        
perror=getCal(myUrl)
if (perror != "OK" ) :
        print ("getCal() failed: "+perror)
        exit
else:               
        ser.write("t0.txt=\"" + str(todayStr) + "\""+e)
        ser.write("t1.txt=\"" + str(tomorrowStr) + "\""+e)
  
