'''
Created on 14 november 2015

@author: federico
'''

import paho.mqtt.client as mosquitto
import json
import urllib,urllib2
import datetime
import threading
import time
from pygame import mixer
from datetime import timedelta


#ALARM SOUND PATH
alarm_path="/home/pi/SmartBed/Smart_Bed/src/Rooster.wav"

#DWEET&FREEBOARD 
thing_name='smart_bed_status'
url_freeboard="https://dweet.io:443/dweet/for/smart_bed_values"
url_status="https://dweet.io:443/get/latest/dweet/for/smart_bed_status"
url_freeboard_qos="https://dweet.io:443/dweet/for/smart_bed_qos"
url_freeboard_sleep_time="https://dweet.io:443/dweet/for/smart_bed_sleep_time"

#THINGSPEAK
url_thingspeak="https://api.thingspeak.com/update"
channel_id="68285"
api_read="XXXXXXXXXXXXXXX"
api_write="ZZZZZZZZZZZZZZZ"

#CONSTANT
soglia=10
broker_ip="127.0.0.1"
smart_alarm_threshold=10 #threshold for the smart alarm:how much movement is needed to ring
sensor_freq=2 #seconds
sensor_MAXVAL=255 #g

#LOCK VARIABLE:this variable is needed to avoid that 2 threads change the status variable
alarm_clock_lock=0

#queue
q=[]
nsamples=10

#status of the system
status=0
mov_tot=0.1
alarm_sensibility=5 #seconds


def on_connect(client,userdata,rc):
    print ("connected with result code"+str(rc))
    client.subscribe("smart_bed/values", 0)
   
        
def on_message(client,userdata,msg):
    print "Raspberry receive data Topic:",msg.topic+'\nMessage:'+str(msg.payload)
    jsonfile=json.loads(msg.payload)
    
    queue_insert(jsonfile)

def queue_insert(jsonfile):
    
    x=int(jsonfile["e"]["v"]["x"])
    y=int(jsonfile["e"]["v"]["y"])
    z=int(jsonfile["e"]["v"]["z"])
    
    valore=transform_function(x, y, z)  
    
    if(valore>soglia):
        q.append(valore-soglia)
        print "Value appended in the queue"+str(valore-soglia)
    else:
        q.append(0)
        print "0 appended"
        
    #SENDING DATA TO FREEBOARD LIVE VIEW
    values={}
    values["x"]=x
    values["y"]=y
    values["z"]=z
    data = urllib.urlencode(values)
    req = urllib2.Request(url_freeboard, data)
    urllib2.urlopen(req)

        
def send_data_c(coda): 
    global mov_tot
    somma=0
    conta=0
    valore=0
    for l in coda:
        if l!=0:
            somma=somma+l 
            conta=conta+1
            
    if somma!=0:  
        valore=float(somma)/conta
        mov_tot=mov_tot+valore
    print "I'm ready to send"+ str(valore)+" to thingspeak"
    
    #sending data to thingspeak movement
    params = urllib.urlencode({'api_key': api_write, 'field1':  "%.2f" % valore})
    req=urllib2.Request(url_thingspeak,params)
    urllib2.urlopen(req)

        
def transform_function(x,y,z):

    #PARAMETERS TO SET IN CASE OF SPECIAL INTEREST IN ONE DIRECTION
    a=1
    b=1
    c=1
    valore=a*x+b*y+z*c
    return valore
  
def process_data(ore,minu,init_time):
    
    global mov_tot
    
    while(status==1):
        if len(q)==nsamples:
            coda=q[:]
            
            tr=threading.Thread(target=send_data_c,args=(coda,))
            tr.start()
            del q[:]

    #LAST DATA IN THE QUEUE
            
    if len(q)!=0:
        coda=q
        tr=threading.Thread(target=send_data_c,args=(coda,))
        tr.start()
        del q[:]
    
    #LAST STATISTICS

    i=datetime.datetime.now() 
    
    #sleep time in minutes
    b=i-init_time
    sleep_time=b.seconds/60
    
    print "Passed seconds from the start"+str(b.seconds)
    print "Total movement"+str(mov_tot)    
    
    #MYFUNCTION TO QUALITY OF SLEEP
    qos=-((100*sensor_freq*nsamples*15/(sensor_MAXVAL*3*b.seconds)))*mov_tot+100
    
    #LAST DATA TO FREEBOARD
   
    data = urllib.urlencode({'qos': "%.0f" %qos})
    req = urllib2.Request(url_freeboard_qos, data)
    urllib2.urlopen(req)

    data = urllib.urlencode({'sleep_time':sleep_time})
    req = urllib2.Request(url_freeboard_sleep_time, data)
    urllib2.urlopen(req)

    #LAST DATA TO THINGSPEAK. WHILE CYCLE IS NEEDED BECAUSE DATA ON THINGSPEAK CAN BE UPDATED EACH 15s
    resp='0'
    times=0
    while resp=='0':
        time.sleep(times)
    	params = urllib.urlencode({'api_key': api_write, 'field2':  "%.1f" % sleep_time})
    	req=urllib2.Request(url_thingspeak,params)
    	risp=urllib2.urlopen(req)
    	resp=risp.read()
    	times=times+5

    resp='0'
    times=0
    while(resp=='0'):
	time.sleep(times)
	params = urllib.urlencode({'api_key': api_write, 'field3':  "%.1f" % qos})
    	req=urllib2.Request(url_thingspeak,params)
    	risp=urllib2.urlopen(req)
    	resp=risp.read()
	times=times+5

   
    
    #needed for next measurement
    mov_tot=0.1
                 
def alarmclock(h,m):
    global alarm_clock_lock
    
    while(status==1):
        i=datetime.datetime.now() 
        if (i.hour==h) & (i.minute==m):
            if alarm_clock_lock==0:
                #LOCK
                alarm_clock_lock=1
                print "ALARM FROM BASIC ALARMCLOCK"
                sound_clock()
                #UNLOCK
                alarm_clock_lock=0
            
        #alarm sensibility        
        time.sleep(alarm_sensibility) 
          
def sound_clock():
    
    mixer.init()
    mixer.music.load(alarm_path)
    while(status==1):
        mixer.music.play()
        time.sleep(4)
        
def smart_alarm(a_h,a_m,ore,minu,smart_min):
    #bad thing but signals cannot be managed as a child thread  
    time_to_wait=abs(a_h-ore)*3600+abs(a_m-abs((minu-smart_min)%60))*60
    print "second to sleep"+str(time_to_wait)
    time.sleep(time_to_wait)
    
    global mov_tot
    initial_mov=mov_tot
    
    while(status==1):
        print "mov_tot"+ str(mov_tot)
        print "initial_mov"+str(initial_mov)
        if((mov_tot-initial_mov)>smart_alarm_threshold):    
            global alarm_clock_lock
            #LOCK
            if alarm_clock_lock==0:
                alarm_clock_lock=1
                print "ALARM FROM SMART CLOCK"
                sound_clock()
                #UNLOCK
                alarm_clock_lock=0
            
        time.sleep(5)
    
    
                  
if __name__ == '__main__':
    
    client=mosquitto.Mosquitto("Raspberry")
    client.on_connect=on_connect
    client.on_message = on_message
  
    client.connect(broker_ip, port=1883, keepalive=60, bind_address="") 
    client.loop_start() 
        
    while(True):
        
        req=urllib2.Request(url_status)
        resp=urllib2.urlopen(req)
        dweet=resp.read()
        dweet2=json.loads(dweet)
        stat=dweet2["with"][0]["content"]["status"]
        
        if (stat==1) & (status==0):
            
            status=1
            print "System is switched ON"
            ore=dweet2["with"][0]["content"]["alarm_hour"]
            minu=dweet2["with"][0]["content"]["alarm_min"]
            smart_min=dweet2["with"][0]["content"]["smart_alarm"]
            
           
	    init_time=datetime.datetime.now() 
            actual_hour=init_time.hour
            actual_min=init_time.minute
            
            t=threading.Thread(target=process_data,args=(actual_hour,actual_min,init_time))
            t.daemon=True
            t.start()
            
            l=threading.Thread(target=alarmclock,args=(ore,minu,))
            l.daemon=True
            l.start()
            
            if(smart_min!=0):
                h=threading.Thread(target=smart_alarm,args=(actual_hour,actual_min,ore,minu,smart_min,))
                h.daemon=True
                h.start()
        
            diz={}
            diz["status"]=1
            val=client.publish("smart_bed",json.dumps(diz) , qos=1)
            
        elif (stat==0) & (status==1):
            
            
            diz={}
            diz["status"]=0
            val=client.publish("smart_bed",json.dumps(diz) , qos=1)
            status=0
            

            print "System is switched OFF"
             
        time.sleep(2)
        
    client.loop_stop()
