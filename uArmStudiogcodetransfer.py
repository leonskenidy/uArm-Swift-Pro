import os
import time

# liftheight=40
# zeropoint=24
liftheight=-2
zeropoint=-1

movespeed=3000
drawspeed=2500

firstpoint=''
isStart=False
with open('C:\\Users\\Wei\\Downloads\\uArm\\gcode\\studiogcode\\tmp_pen.gcode', 'r') as f:
    with open('C:\\Users\\Wei\\Downloads\\uArm\\gcode\\studiogcode\\tmp_pen1.gcode', 'w') as f1:
        for line in f.readlines():
            if(line.strip() =='G0 Z20.00 F2500.00' and not isStart):
                isStart=True
                firstpoint=''        
            if(line.strip() !='G0 Z20.00 F2500.00' and isStart):
                isStart=False
                firstpoint=line.replace('G0','G1').replace('F2500.00','F500.00')
                print(firstpoint)

            if(line!=firstpoint):
                line=line.replace('Z20.00','Z' + str(liftheight))  
                line=line.replace('Z0.00','Z' + str(zeropoint))

                line=line.replace('F2500.00','F' + str(movespeed))
                line=line.replace('F500.00','F' + str(drawspeed))
                            
                f1.writelines(line)
            else:
                print(line)
        f1.close()
    f.close()