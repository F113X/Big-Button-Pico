from machine import Pin, ADC
import time

#outputs
out0 = Pin(0, Pin.OUT)
out1 = Pin(1, Pin.OUT)
out2 = Pin(2, Pin.OUT)
out3 = Pin(3, Pin.OUT)
out4 = Pin(4, Pin.OUT)
out5 = Pin(5, Pin.OUT)

#inputs
dlt = Pin(6, Pin.IN) #delete
rst = Pin(7, Pin.IN) #reset
fll = Pin(8, Pin.IN) #fill
clr = Pin(9, Pin.IN) #clear
clk = Pin(10, Pin.IN) #clock
trig = Pin(11, Pin.IN) #big button

#analogue Inputs
trk = ADC(26) #track Select
stepLen = ADC(27) #step length

#main sequence
seq = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

#fill sequence
fill = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

currentSeq = seq

#trigger
def trigger(track, step, seqNum):
    if trig.value() == 1:
        if seqNum == 0:
            seq[track][step] = 1
        elif seqNum == 1:
            fill[track][step] = 1

#fill (second sequence)
def fill():
    if fll.value() == 0:
        currentSeq = seq
        seqNum = 0

    elif fll.value() == 1:
        currentSeq = fill
        seqNum = 1
    
    return seqNum

#delete step
def delete(track, step):
    if dlt.value() == 0:
        currentSeq[track][step] = 0

#clear track
def clear(track):
    if clr.value() == 0:
        for i in range(32):
            currentSeq[track][i] = 0

#reset sequence
def reset():
    if rst.value() == 0:
        for i in range(6):
            for j in range(32):
                currentSeq[i][j] = 0
                
#track select
def trackSelect():
    value = trk.read_u16() / 65536
    
    if value < 1/6:
        return 0
    if value >= 1/6 and value < 2/6:
        return 1
    if value >= 2/6 and value < 3/6:
        return 2
    if value >= 3/6 and value < 4/6:
        return 3
    if value >= 4/6 and value < 5/6:
        return 4
    if value >= 5/6:
        return 5

#output thing
def out(length, step):
    out0.value(currentSeq[0][step])
    out1.value(currentSeq[1][step])
    out2.value(currentSeq[2][step])
    out3.value(currentSeq[3][step])
    out4.value(currentSeq[4][step])
    out5.value(currentSeq[5][step])
    time.sleep(length)
    out0.value(0)
    out1.value(0)
    out2.value(0)
    out3.value(0)
    out4.value(0)
    out5.value(0)

#main code
def main(currentSeq):
    step = 0
    
    while True:
        length = stepLen.read_u16() / 65536
        reset()
        seqNum = fill()
        if seqNum == 0:
            currentSeq = seq
            
        elif seqNum == 1:
            currentSeq = fill
            
        
        
        track = trackSelect()
        #track = 0
        trigger(track, step, seqNum)
        delete(track,step)
        clear(track)
        #print(trackSelect())
        
        if clk.value() == 1:
            out(length, step)
            
            step += 1
            if step == 32:
                step = 0
        

main(currentSeq)

