from statistics import mean
import numpy as np
import time


class  SignalStates:
    GREEN = 0 
    NUMBER_OF_SEGMENT = 3

class State:
    def get_current_time(self):
        """
        This function returns the current time in seconds
        :return: The current time in seconds since the Epoch.
        """
        return time.time()
    
    def get_delay(self,Time_sent): # (5) 6
        """
        The function get_delay() returns the difference between the current time and the time the
        message was sent
        
        :param Time_sent: The time the message was sent
        :return: The time difference between the current time and the time the message was sent.
        """
        return self.get_current_time() - Time_sent
    
    def get_distance(self,Time_sent,Speed_sent):
        """
        Time_sent (tsent) : The timestamp of a message sent by a vehicle
        Speed_sent (ssent) : Vehicle speed at timestamp tsent 
        """
        return self.get_delay(Time_sent)*Speed_sent

    def get_position(self,angle,length_lane,vehicle_state,State_signal,XPosition_sent,YPosition_sent,Time_sent,Speed_sent,x_start_lane,y_start_lane,vehicle_length=None,Gap=None,PSpeed_sent=None,Px_pos_vehicals=None,Py_pos_vehicals=None):
        """
        The function takes in the current position of the vehicle, the current state of the signal, the
        current speed of the vehicle, the current time, the current angle of the vehicle, the length of
        the lane, the starting position of the lane, the length of the vehicle, the gap between the
        vehicle and the vehicle in front of it, the speed of the vehicle in front of it, the x and y
        position of the vehicle in front of it, and returns the expected x and y position of the vehicle
        
        :param angle: the angle of the lane
        :param length_lane: length of the lane
        :param vehicle_state: 0 = no vehicle in front, 1 = vehicle in front
        :param State_signal: 1 = green, 0 = red
        :param XPosition_sent: The current x position of the vehicle
        :param YPosition_sent: The current Y position of the vehicle
        :param Time_sent: time in seconds
        :param Speed_sent: The speed of the vehicle
        :param x_start_lane: the x coordinate of the start of the lane
        :param y_start_lane: the y-coordinate of the start of the lane
        :param vehicle_length: length of the vehicle
        :param Gap: The distance between the vehicle and the vehicle in front of it
        :param PSpeed_sent: The speed of the vehicle in front of the vehicle in question
        :param Px_pos_vehicals: The x position of the vehicle in front of the vehicle in question
        :param Py_pos_vehicals: The y position of the vehicle in front of the vehicle in question
        :return: the expected position of the vehicle.
        """
        ExpectedXPositiion,ExpectedYPositiion = XPosition_sent,YPosition_sent
        if State_signal==1 : # State_signal is 1 = Green
            if angle==90:ExpectedXPositiion=XPosition_sent+self.get_distance(Time_sent,Speed_sent)
            elif angle==270:ExpectedXPositiion=XPosition_sent-self.get_distance(Time_sent,Speed_sent)
            elif angle==0:ExpectedYPositiion=YPosition_sent+self.get_distance(Time_sent,Speed_sent)
            elif angle==180:ExpectedYPositiion=YPosition_sent-self.get_distance(Time_sent,Speed_sent)
        else:
            if vehicle_state == 0:
                if (abs(abs(ExpectedXPositiion)-abs(x_start_lane))>2.0)or(abs(abs(ExpectedYPositiion)-abs(y_start_lane))>2.0):
                    if angle == 90 :ExpectedXPositiion=XPosition_sent+self.get_distance(Time_sent,Speed_sent)
                    elif angle == 270:ExpectedXPositiion=XPosition_sent-self.get_distance(Time_sent,Speed_sent)
                    elif angle == 0:ExpectedYPositiion=YPosition_sent+self.get_distance(Time_sent,Speed_sent)
                    elif angle == 180:ExpectedYPositiion=YPosition_sent-self.get_distance(Time_sent,Speed_sent)
            else:
                if angle == 90 :
                    ExpectedXPositiion=XPosition_sent+self.get_distance(Time_sent,Speed_sent)
                    if (ExpectedXPositiion>0 and ExpectedXPositiion<Px_pos_vehicals)or(ExpectedXPositiion<0 and ExpectedXPositiion>Px_pos_vehicals):pass 
                    else:ExpectedXPositiion = XPosition_sent
                elif angle == 270:
                    ExpectedXPositiion=XPosition_sent-self.get_distance(Time_sent,Speed_sent)
                    if (ExpectedXPositiion>0 and ExpectedXPositiion<Px_pos_vehicals)or(ExpectedXPositiion<0 and ExpectedXPositiion > Px_pos_vehicals):pass 
                    else:ExpectedXPositiion = XPosition_sent
                elif angle == 0:
                    ExpectedYPositiion=YPosition_sent+self.get_distance(Time_sent,Speed_sent)
                    if (ExpectedYPositiion>0 and ExpectedYPositiion<Py_pos_vehicals)or(ExpectedYPositiion<0 and ExpectedYPositiion > Px_pos_vehicals):pass 
                    else:ExpectedYPositiion = YPosition_sent                    
                elif angle == 180:
                    ExpectedYPositiion=YPosition_sent-self.get_distance(Time_sent,Speed_sent)
                    if (ExpectedYPositiion>0 and ExpectedYPositiion<Py_pos_vehicals)or(ExpectedYPositiion<0 and ExpectedYPositiion > Py_pos_vehicals):pass 
                    else:ExpectedYPositiion=YPosition_sent                    
        return ExpectedXPositiion , ExpectedYPositiion   

    def lane_segmentation(self,length_lane,x_start_lane,y_start_lane,x_end_lane,y_end_lane,angel):
        """
        It takes the start and end points of a line, and divides it into a number of segments
        
        :param length_lane: the length of the lane
        :param x_start_lane: x coordinate of the start of the lane
        :param y_start_lane: the y coordinate of the start of the lane
        :param x_end_lane: x coordinate of the end of the lane
        :param y_end_lane: the y coordinate of the end of the lane
        :param angel: the angle of the lane
        :return: the start and end points of the segments of the lane.
        """
        length_seg = length_lane/SignalStates.NUMBER_OF_SEGMENT
        x_start_segments,y_start_segments,x_end_segments,y_end_segments = [],[],[],[]
        for i in range(SignalStates.NUMBER_OF_SEGMENT):
            if angel==270 or angel==90 :
                x_start,x_end=x_start_lane,x_start_lane+length_seg if x_start_lane < x_end_lane else x_start_lane-length_seg
                x_start_segments.append(x_start)
                y_start_segments.append(y_start_lane)
                x_end_segments.append(x_end)
                y_end_segments.append(y_end_lane)
                x_start_lane = x_end
            elif angel == 0 or angel == 180:
                y_start,y_end=y_start_lane,y_start_lane+length_seg if y_start_lane < y_end_lane else y_start_lane-length_seg
                x_start_segments.append(x_start_lane)
                y_start_segments.append(y_start)
                x_end_segments.append(x_end_lane)
                y_end_segments.append(y_end)
                y_start_lane = y_end
        if len(x_start_segments)==0:
            x_start_segments=np.zeros(SignalStates.NUMBER_OF_SEGMENT).tolist()
            x_end_segments,y_start_segments,y_end_segments=x_start_segments.copy(),x_start_segments.copy(),x_start_segments.copy()
        return x_start_segments,y_start_segments,x_end_segments,y_end_segments

    def vehicle_distribution_to_segments(self,x_pos_vehicals,y_pos_vehicals,length_lane,x_start_lane,y_start_lane,x_end_lane,y_end_lane,angel,vehicles_arrangement,State_signal,Time_sent,Speed_sent,vehicle_length,Gap,with_predicted_position):
        """
        It takes the position of the vehicles, the length of the lane, the start and end points of the
        lane, the angel of the lane, the arrangement of the vehicles, the state of the signal, the time
        the signal was sent, the speed of the vehicle, the length of the vehicle, the gap between the
        vehicles, and a boolean value that indicates whether the predicted position of the vehicle
        should be used or not
        
        :param x_pos_vehicals: x-coordinates of the vehicles
        :param y_pos_vehicals: The y-coordinates of the vehicles
        :param length_lane: length of the lane
        :param x_start_lane: x coordinate of the start of the lane
        :param y_start_lane: The y-coordinate of the start of the lane
        :param x_end_lane: x coordinate of the end of the lane
        :param y_end_lane: The y coordinate of the end of the lane
        :param angel: the angle of the lane
        :param vehicles_arrangement: 0 for the first vehicle in the lane, 1 for the rest
        :param State_signal: The state of the signal (0: red, 1: green)
        :param Time_sent: The time the vehicle sent its message
        :param Speed_sent: the speed of the vehicle
        :param vehicle_length: length of the vehicle
        :param Gap: The distance between the vehicle and the vehicle in front of it
        :param with_predicted_position: if True, the function will use the predicted position of the
        vehicle to determine which segment it is in. If False, it will use the actual position of the
        vehicle
        :return: The number of vehicles in each segment, the x and y positions of the vehicles.
        """
        x_start_segments,y_start_segments,x_end_segments,y_end_segments = self.lane_segmentation(length_lane,x_start_lane,y_start_lane,x_end_lane,y_end_lane,angel)
        num_vehicals_in_segment = np.zeros(len(x_start_segments))
        for i,_ in enumerate(x_pos_vehicals):
            if with_predicted_position:
                if vehicles_arrangement[i] == 0 :
                    x_pos_vehicals[i] ,y_pos_vehicals[i]=self.get_position(angel,length_lane,vehicles_arrangement[i],State_signal,x_pos_vehicals[i],y_pos_vehicals[i],Time_sent[i],Speed_sent[i],x_start_lane,y_start_lane,vehicle_length[i],Gap[i])
                else:
                    x_pos_vehicals[i] ,y_pos_vehicals[i]=self.get_position(angel,length_lane,vehicles_arrangement[i],State_signal,x_pos_vehicals[i],y_pos_vehicals[i],Time_sent[i],Speed_sent[i],x_start_lane,y_start_lane,vehicle_length[i],Gap[i],Speed_sent[i-1],x_pos_vehicals[i-1],y_pos_vehicals[i-1])
            if angel==90 :
                for j,_ in enumerate(x_start_segments):
                    if x_pos_vehicals[i]>x_end_segments[j]:
                        num_vehicals_in_segment[j]+=1
                        break
            elif angel==270 :
                for j,_ in enumerate(x_start_segments):
                    if x_pos_vehicals[i]<x_end_segments[j]:
                        num_vehicals_in_segment[j]+=1
                        break  
            elif angel==0 :
                for j,_ in enumerate(y_start_segments):
                    if y_pos_vehicals[i]>y_end_segments[j]:
                        num_vehicals_in_segment[j]+=1
                        break
            elif angel==180 :
                for j,_ in enumerate(y_start_segments):
                    if y_pos_vehicals[i]<y_end_segments[j]: 
                        num_vehicals_in_segment[j]+=1
                        break
        return num_vehicals_in_segment.tolist() , x_pos_vehicals , y_pos_vehicals

    def state(self,messeges,with_predicted_position):
        """
        It takes a list of lists, and returns a list of lists
        
        :param messeges: a list of lists, each list contains the following parameters:
        :param with_predicted_position: This is a boolean value that determines whether the state is
        calculated with the predicted position of the vehicles or not
        :return: The state is being returned.
        """
        matric1,matric2,matric3,matric4 = [],[],[],[]
        for messeg in messeges:
            x_pos_vehicals,y_pos_vehicals,length_lane,x_start_lane,y_start_lane,x_end_lane,y_end_lane,angel,vehicles_arrangement,State_signal,Time_sent,Speed_sent,vehicle_length,Gap,acceleration,number_neighbor,speed_neighbor,acc_neighbor = messeg[0],messeg[1],messeg[2],messeg[3],messeg[4],messeg[5],messeg[6],messeg[7],messeg[8],messeg[9],messeg[10],messeg[11],messeg[12],messeg[13],messeg[14],messeg[15],messeg[16],messeg[17]
            
            num_vehicals_in_segment,new_x_pos_vehicals , new_y_pos_vehicals = self.vehicle_distribution_to_segments(x_pos_vehicals,y_pos_vehicals,length_lane,x_start_lane,y_start_lane,x_end_lane,y_end_lane,angel,vehicles_arrangement,State_signal,Time_sent,Speed_sent,vehicle_length,Gap,with_predicted_position)

            matric3.append(num_vehicals_in_segment)
            matric3.append(number_neighbor)
            matric4.append(State_signal)
            temp = 0 
            for num in num_vehicals_in_segment:
                num = int(num)
                t = Speed_sent[temp:num+temp]
                matric1.append(mean(t) if len(t)>0 else 0)
                t = acceleration[temp:num+temp]
                matric2.append(mean(t) if len(t)>0 else 0)
                temp = num
            matric1.append(speed_neighbor)
            matric2.append(acc_neighbor)
        matric1,matric2 = np.concatenate(matric1, axis=None),np.concatenate(matric2, axis=None)
        matric3,matric4 = np.concatenate(matric3, axis=None),np.concatenate(matric4, axis=None)
        finall_state = np.concatenate([matric1,matric2,matric3,matric4], axis=None)
        return np.reshape(finall_state, (1,-1)) #.squeeze()
