#!/usr/bin/env python	
#-*- coding:utf-8 -*-	# 한글 주석을 달기 위해 사용한다.

import rospy
from sensor_msgs.msg import Joy
import random

class RandomJoyNode:
    def __init__(self):
        self.pub = rospy.Publisher("joy", Joy, queue_size=10)
        self.rate = rospy.Rate(30) # 30hz
        
        self.last_vel_x_select_secs = 0;
        self.last_vel_y_select_secs = 0;
        self.last_vel_w_select_secs = 0;
        
        self.vel_x_duration = 0;
        self.vel_y_duration = 0;
        self.vel_w_duration = 0;
        
        self.vel_x = 0.0;
        self.vel_y = 0.0;
        self.vel_w = 0.0;
    
    def random_velocity(self, current_time): 

        
        
        if current_time > self.last_vel_x_select_secs + self.vel_x_duration:
            self.last_vel_x_select_secs = current_time
            self.vel_x_duration = random.uniform(1, 5)
            self.vel_x = random.random()
            
        if current_time > self.last_vel_y_select_secs + self.vel_y_duration:
            self.last_vel_y_select_secs = current_time
            self.vel_y_duration = random.uniform(1, 5)
            self.vel_y = random.random()
        
        if current_time > self.last_vel_w_select_secs + self.vel_w_duration:
            self.last_vel_w_select_secs = current_time
            self.vel_w_duration = random.uniform(1, 5)
            self.vel_w = random.random()
        
        
        return [self.vel_y, self.vel_x, 0.0, self.vel_w, 0.0, 0,0, 0,0, 0,0, 0,0]  
     
    def main(self):
        joy_msg = Joy()	# 메시지 변수 선언
        count = 0		# 코드에서 사용할 변수 선언
        joy_msg.axes = [0,0,0,0,0,0,0,0]
        joy_msg.buttons = [0,0,0,0,0,0,0,0,0,0,0]
        # 중단되거나 사용자가 강제종료(ctrl+C) 전까지 계속 실행
        while not rospy.is_shutdown():
            joy_msg.header.stamp = rospy.Time.now()	#현재 시각 담음
            joy_msg.header.seq = count		# count 변수 값 담음
            # joy_msg.axes = self.random_velocity(joy_msg.header.stamp.secs)
            joy_msg.axes[0] = 1.0
            joy_msg.axes[1] = 1.0
            joy_msg.axes[3] = 1.0
            # 터미널에 출력
            # rospy.loginfo("send time(sec) = %d", joy_msg.header.stamp.secs)
            # rospy.loginfo("send seq = %d", joy_msg.header.seq)
            
            # 메시지를 퍼블리시
            self.pub.publish(joy_msg)
            
            # 정해둔 주기(hz)만큼 일시중단
            self.rate.sleep()

            count += 1
    

        

if __name__ == '__main__':
    rospy.init_node('random_joy_command')
    node = RandomJoyNode()
    try:
        node.main()
    except rospy.ROSInterruptException:
        pass