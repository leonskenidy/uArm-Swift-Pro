# -*- coding: UTF-8 -*-

import os
import time
from decimal import Decimal
from uarm.wrapper import SwiftAPI

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})

swift.waiting_ready()
device_info = swift.get_device_info()
print(device_info)
firmware_version = device_info['firmware_version']
# if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
#     swift.set_speed_factor(0.00005)


isOffisite=False    # true will add center value, false is absolute pos
# isOffisite = input("Is Offset")
pos = swift.get_position()
pen_tip_height = pos[2]
center={'x':pos[0],'y':pos[1],'z':pen_tip_height+25}
if(isOffisite):
    print('解锁电机')
    swift.set_servo_detach()
    input('笔尖接触桌面')
    # swift.set_buzzer()


    print('锁上电机')
    swift.set_servo_attach()
    pos = swift.get_position()
    print('pos', pos)  # pos [225.41, 16.28, 38.16]
    pen_tip_height = pos[2]
    center={'x':pos[0],'y':pos[1],'z':pen_tip_height+25}
    print('pen_tip_height')
    print(pen_tip_height)
    print('center')
    print(center)

swift.set_mode(3)
# swift.send_cmd_sync('M2400 S3')
# swift.send_cmd_sync('M2201 3')

# print(swift.get_servo_attach(servo_id=0))
# print(swift.get_servo_attach(servo_id=1))
# print(swift.get_servo_attach(servo_id=2))
# print(swift.get_servo_attach(servo_id=3))

# print(swift.set_servo_attach(servo_id=3))

# swift.set_wrist(angle=90)
# swift.flush_cmd(wait_stop=True)
print("Read gcode")
with open("gcode\\optimize prime1.gcode", "r") as f:
    # print ("文件名: ", f.name);
    # # f.write("这是我创建的第一个测试文件！\nwelcome!");
    # print (f.tell());
    # #输出当前指针位置
    # f.seek(os.SEEK_SET);
    # #设置指针回到文件最初
    # context = f.read();
    # print (context);
    # # f.close();    
   
    for line in f.readlines():                      #依次读取每行
        offsite=''
        result = list()     
        x=0
        y=0
        line = line.strip()                             #去掉每行头尾空白
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行
            continue                                    #是的话，跳过不处理
        # print(line)                                     #保存
        result=line.split(' ')
        for cmd in result:
            if(not cmd.find('X') and isOffisite):
                x=center['x'] + float(cmd[cmd.index('X')+1:])
                cmd='X'+ str(Decimal(str(x)).quantize(Decimal('0.00')))
            if(not cmd.find('Y') and isOffisite):
                y=center['y'] + float(cmd[cmd.index('Y')+1:])
                cmd='Y'+ str(Decimal(str(y) ).quantize(Decimal('0.00')))
            if(not cmd.find('Z')):
                try:
                    # z=center['z'] + float(cmd[cmd.index('Z')])
                    if(float(cmd[cmd.index('Z')+1:])==-1 and isOffisite):  #zero point
                        cmd='Z'+str(pen_tip_height)                        
                    elif (float(cmd[cmd.index('Z')+1:])==-2 and isOffisite):  #pen lift height
                        cmd='Z'+str(pen_tip_height+10)
                    # if(float(cmd[cmd.index('Z')+1:])==-3):  #zero point with pen move height
                    #     z=pen_tip_height - float(cmd[cmd.index('Z')+1:])
                    #     cmd='Z'+str(z)
                    elif(isOffisite):
                        z=pen_tip_height - float(cmd[cmd.index('Z')+1:])
                        cmd='Z'+ str(Decimal(str(z)).quantize(Decimal('0.00')))

                except Exception as e:
                    print(e) 
            offsite+=cmd+' '
        print(offsite.strip())
        swift.send_cmd_sync(offsite.strip())
    # reset
    swift.send_cmd_sync('G0 X103 Y0 Z42')
    swift.flush_cmd()
    time.sleep(5)
    swift.disconnect()
    