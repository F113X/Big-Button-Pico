# Big-Button-Pico-Code

**Note: Because buttons are inverted, some code is inverted as well to cope with that. Please change it if using other buttons.**

**Another Note: This code may still have problems. It mostly works, but has not been fully tested yet.**

## Overall Logic
### Modules used
From machine: Pin, ADC
time (utime)

### Variables
#### Pin outputs
|Variable Name|Pin Number|Function|
|-------------|----------|--------|
|out0|0|Track 1 output|
|out1|1|Track 2 output|
|out2|2|Track 3 output|
|out3|3|Track 4 output|
|out4|4|Track 5 output|
|out5|5|Track 6 output|

#### Pin inputs
|Variable Name|Pin Number|Function|
|-------------|----------|--------|
|dlt|6|Delete current step on current track|
|rst|7|Reset the whole sequence|
|fll|8|Switch to fill sequence|
|clr|9|Clear current track|
|clk|10|Clock input|
|trig|11|Big button trigger|

#### Analogue pins
|Analogue Input|Pin Number|Function|
|--------------|----------|--------|
|trk|26|Track Select|
|stepLen|27|Step Length|

#### Arrays
|Array Name|Function|
|----------|--------|
|seq|Main sequence|
|fill|Fill sequence|
|currentSeq|Currently played sequence|

### Functions
##
```
trigger(track, step, seqNum)
```
Description: switching a specific step on a specific track on a specific sequence

Input Variables:
|Variable|Range|Definition|
|--------|-----|----------|
|track|0-5|Selects a track|
|step|0-31|Selects a step|
|seqNum|0-1|Selects a sequence (0 = main sequence, 1 = fill sequence)

Logic:
```
If trig is 0:
    If seqNum is 0, seq[track][step] = 1
    If seqNum is 1, fill[track][step] = 1
```

## 
```
fill()
```
Description: switch between the fill and normal sequence

Logic: 
```
If fill is 1, currentSeq = fill; seqNum = 1
If fill is 0, currentSeq = seq; seqNum = 0
Return seqNum
```

##
```
delete(track, step)
```
Description: delete the step on a specific step in a specific track

Input Variables:
|Variable|Range|Definition|
|--------|-----|----------|
|track|0-5|Selects a track|
|step|0-31|Selects a step|

Logic:
```
If dlt is 0: currentSeq[track][step] = 0
```

##
```
clear(track)
```
Description: delete all steps on the selected track

Input Variables:
|Variable|Range|Definition|
|--------|-----|----------|
|track|0-5|Selects a track|

Logic:
```
If clr is 0:
    For i In Range 32: currentSeq[track][i] = 0
```

##
```
reset()
```
Description: reset the whole sequence

Logic:
```
If rst is 1:
    For i In Range 6:
        For j In Range 32: currentSeq[i][j] = 0
```

##
```
trackSelect()
```
Description: function for selecting the track

Logic:
```
value = trk.Read_u16() / 65536
If value is smaller than 1/6: return 0
If value is larger or equal to 1/6 and value is smaller than 2/6: return 1
If value is larger or equal to 2/6 and value is smaller than 3/6: return 2
If value is larger or equal to 3/6 and value is smaller than 4/6: return 3
If value is larger or equal to 4/6 and value is smaller than 5/6: Return 4
If value is larger than  5/6: Return 5
```

##
```
out(length, step)
```
Description: output the value of current step

Input Variables:
|Variable|Range|Definition|
|--------|-----|----------|
|length|0-1|Sets gate length|
|step|0-31|Selects a step|

Logic:
```
out0 = currentSeq[0][step]
out1 = currentSeq[1][step]
out2 = currentSeq[2][step]
out3 = currentSeq[3][step]
out4 = currentSeq[4][step]
out5 = currentSeq[5][step]
time.sleep(length)
out0 = 0
out1 = 0
out2 = 0
out3 = 0
out4 = 0
out5 = 0
```

##
```
main()
```
Description: main function for sequencer

Logic:
```
step = 0
    
while True:
    length = stepLen.read_u16() / 65536
    reset()
    seqNum = fill()
    track = trackSelect()
    trigger(track, step, seqNum)
    delete(track,step)
    clear(track)
        
    If clk Is 1:
        out(length, step)
        step = step + 1
        If step Is 32: step = 0
```