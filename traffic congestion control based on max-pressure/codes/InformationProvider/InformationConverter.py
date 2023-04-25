from codes.Environment.configuration import Vehicle_characteristics
from traci import trafficlight as t
from traci import lane as l
import math


class InfromationConverter:

    def __init__(self,controlle_messege_geter):
        self.controlle_messege_geter = controlle_messege_geter
        self.lane_info = {}

    def setattr(self,lane_info):
        self.lane_info = lane_info

    def get_start_lane(self,inter_id,lane_id):
        """
        It returns the start point of a lane
        
        :param inter_id: the id of the intersection
        :param lane_id: the id of the lane
        :return: The start point of the lane.
        """
        try:e_point = self.lane_info[inter_id][lane_id]['start_point']
        except: e_point = l.getShape(lane_id)[0]
        return e_point

    def get_end_lane(self,inter_id,lane_id):
        """
        It returns the end point of a lane
        
        :param inter_id: the id of the intersection
        :param lane_id: the id of the lane
        :return: The end point of the lane.
        """
        try:s_point = self.lane_info[inter_id][lane_id]['end_point']
        except:s_point = l.getShape(lane_id)[-1]
        return s_point

    def get_lane_length(self,inter_id,lane_id):
        """
        It returns the length of a lane
        
        :param inter_id: the id of the intersection
        :param lane_id: the id of the lane
        :return: The length of the lane.
        """
        try:s_point = self.lane_info[inter_id][lane_id]['lane_length']
        except:s_point = l.getLength(lane_id)
        return s_point

    def get_right_leading_lane(self,inter_id,lane_id):
        """
        It tries to get the right leading lane from the lane_info dictionary, and if it fails, it calls
        the lanes_leading function from the controlle_messege_geter object
        
        :param inter_id: intersection id
        :param lane_id: the lane id of the lane you want to get the information of
        :return: The lane_id of the right leading lane.
        """
        try:t = self.lane_info[inter_id][lane_id]['right_leading_lane']
        except:_,t,_ = self.controlle_messege_geter.lanes_leading(lane_id,by_vehicle=False)
        return t

    def get_straight_leading_lane(self,inter_id,lane_id):
        """
        It tries to get the right leading lane of a lane, if it fails, it gets the right leading lane of
        the lane by vehicle
        
        :param inter_id: intersection id
        :param lane_id: the lane id of the current lane
        :return: The lane_id of the lane that is to the right of the current lane.
        """
        try:t = self.lane_info[inter_id][lane_id]['right_leading_lane']
        except:_,_,t = self.controlle_messege_geter.lanes_leading(lane_id,by_vehicle=False)
        return t

    def get_number_of_vehical(self,inter_id,lane_id):
        """
        It returns the number of vehicles in a lane
        
        :param inter_id: The id of the intersection
        :param lane_id: The lane id of the lane you want to get the number of vehicles from
        :return: The number of vehicles in the lane.
        """
        n = 0
        try:n = self.lane_info[inter_id][lane_id]['number_of_vehical']
        except:pass
        return n

    def get_number_of_places_available(self,inter_id,lane_id):
        """
        It returns the number of places available in a lane
        
        :param inter_id: the id of the intersection
        :param lane_id: the id of the lane
        :return: The number of places available in the lane.
        """
        n = 0 
        try:n = self.lane_info[inter_id][lane_id]['number_of_places_available']
        except:n = l.getLength(lane_id)/(Vehicle_characteristics['length']+Vehicle_characteristics['min_cap'])
        return n

    def get_num_veh_neighbor_lane(self,inter_id,lane_id):
        """
        > This function returns the number of vehicles in the neighboring lane of the lane specified by
        the lane_id parameter
        
        :param inter_id: intersection id
        :param lane_id: the lane id of the lane that the vehicle is on
        :return: The number of vehicles in the neighboring lane.
        """
        n = 0
        try:n = self.lane_info[inter_id][lane_id]['num_veh_neighbor_lane']
        except:pass
        return n

    def get_avg_speed_veh_neighbor_lane(self,inter_id,lane_id):
        """
        It returns the average speed of vehicles in the neighboring lane of the lane specified by the
        lane_id parameter
        
        :param inter_id: intersection id
        :param lane_id: the lane id of the lane you want to get the information for
        :return: The average speed of the vehicles in the neighboring lane.
        """
        spd = 0
        try: spd = self.lane_info[inter_id][lane_id]['avg_speed_veh_neighbor_lane']
        except:pass
        return spd

    def get_avg_acceleration_veh_neighbor_lane(self,inter_id,lane_id):
        """
        It returns the average acceleration of vehicles in the neighboring lane of the lane specified by
        the lane_id parameter
        
        :param inter_id: intersection id
        :param lane_id: the lane id of the lane you want to get the information for
        :return: The average acceleration of the vehicles in the neighboring lane.
        """
        acc = 0
        try:acc = self.lane_info[inter_id][lane_id]['avg_acceleration_veh_neighbor_lane']
        except:pass
        return acc

    def get_number_of_vehicles_moving_from_straight_lane(self,inter_id,lane_id):
        """
        It returns the number of vehicles moving from a straight lane
        
        :param inter_id: The intersection ID
        :param lane_id: The lane id of the lane that the vehicle is currently on
        :return: The number of vehicles moving from straight lane.
        """
        n = 0
        try:n = self.lane_info[inter_id][lane_id]['number_of_vehicles_moving_from_straight_lane']
        except:pass
        return n

    def get_number_of_vehicles_moving_from_right_lane(self,inter_id,lane_id):
        """
        It returns the number of vehicles moving from the right lane
        
        :param inter_id: The id of the intersection
        :param lane_id: The lane id of the lane you want to get the information for
        :return: The number of vehicles moving from the right lane.
        """
        n = 0 
        try:n = self.lane_info[inter_id][lane_id]['number_of_vehicles_moving_from_right_lane']
        except:pass
        return n

    def get_Angle(self,inter_id,lane_id):
        """
        It returns the angle of the lane, if it's not in the dictionary, it calculates it and adds it to
        the dictionary
        
        :param inter_id: the id of the intersection
        :param lane_id: the id of the lane
        :return: The angle of the lane.
        """
        angle = 0 
        try:angle = self.lane_info[inter_id][lane_id]['Angle']
        except:
            shap_of_lane = l.getShape(lane_id)
            start_point,end_point = shap_of_lane[-1] , shap_of_lane[0]
            x,y = start_point[1]-end_point[1] , start_point[0]-end_point[0]
            angle = math.atan2(y,x)*(180/math.pi)
            angle = 270 if angle == -90 else angle
        return angle

    def get_state(self,inter_id,lane_id):
        """
        It returns the state of the lane
        
        :param inter_id: the id of the intersection
        :param lane_id: the lane id of the lane you want to get the state of
        :return: The state of the lane.
        """
        s = 0
        try:s = self.lane_info[inter_id][lane_id]['state']
        except:pass
        return s

    def get_lanes_in_intersction(self,intersection_id):
        """
        It takes the intersection id as input and returns the list of lanes that are controlled by the
        intersection
        
        :param intersection_id: the id of the intersection
        :return: a list of lane ids that are controlled by the intersection.
        """
        controlled_lanes,temp = t.getControlledLanes(intersection_id),[]
        for i,lane_id in enumerate(controlled_lanes):
            if i%2==0:temp.append(lane_id)
        return temp

    def get_lane_state(self,lane_id):
        """
        > It returns the state of a lane, given the lane id
        
        :param lane_id: the lane id of the lane you want to get the state of
        :return: The state of the lane.
        """
        s=0
        try:
            for inter in self.lane_info:
                try:s = self.get_state(inter,lane_id) if lane_id in self.lane_info[inter] else 0
                except:pass
        except:pass
        return s
    
    def get_number_of_v(self,lane_id):
        """
        It returns the number of vehicles in a lane
        
        :param lane_id: The lane ID of the lane for which to retrieve the number of vehicles
        :return: The number of vehicles in the lane.
        """
        n=0
        try:
            for inter in  self.lane_info:
                try:n = self.get_number_of_vehical(inter,lane_id) if lane_id in self.lane_info[inter] else 0
                except:pass
        except:pass
        return n

    def get_number_of_vehical_in_lane(self,intersection_id,lanes_ids):
        """
        It tries to get the number of vehicles in a lane, and if it fails, it returns 0
        
        :param intersection_id: the id of the intersection
        :param lanes_ids: list of lane ids
        :return: The number of vehicles in the lane.
        """
        try:number_of_vehical_of_all_lane = self.get_number_of_vehical(intersection_id,lanes_ids)
        except:number_of_vehical_of_all_lane = [0]
        return number_of_vehical_of_all_lane
    
    def get_Xposition_for_all_vehicals_in_lane(self,intersection_id,lanes_ids):
        """
        It returns a list of all the X positions of all the vehicles in a lane
        
        :param intersection_id: The id of the intersection
        :param lanes_ids: list of lane ids
        :return: The X position of all vehicles in the lane.
        """
        try:all_pos = self.lane_info[intersection_id][lanes_ids]['X_position']
        except:all_pos = [0]
        return all_pos
    
    def get_Yposition_for_all_vehicals_in_lane(self,intersection_id,lanes_ids):
        """
        It returns a list of all the Y positions of all the vehicles in a lane
        
        :param intersection_id: The id of the intersection
        :param lanes_ids: list of lanes ids
        :return: The Y position of all vehicles in the lane.
        """
        try:all_pos = self.lane_info[intersection_id][lanes_ids]['Y_position']
        except:all_pos = [0]
        return all_pos

    def get_speed_for_all_vehicals_in_lane(self,intersection_id,lanes_ids):
        """
        It returns the speed of all vehicles in a lane
        
        :param intersection_id: The id of the intersection
        :param lanes_ids: list of lane ids
        :return: The speed of all vehicles in the lane.
        """
        try:all_speed = self.lane_info[intersection_id][lanes_ids]['vehicles_speed']
        except:all_speed = [0]
        return all_speed

    def get_time_send_for_all_vehicals_in_lane(self,intersection_id,lanes_ids):
        """
        It returns a list of all the times that a vehicle has been sent through a lane
        
        :param intersection_id: The id of the intersection
        :param lanes_ids: list of lane ids
        :return: The time that the vehicle was sent.
        """
        try:all_times = self.lane_info[intersection_id][lanes_ids]['Times_send']
        except:all_times = [0]
        return all_times

    def get_vehicle_length_for_all_vehicals_in_lane(self,intersection_id,lanes_ids):
        """
        It returns the length of all vehicles in a lane
        
        :param intersection_id: The id of the intersection
        :param lanes_ids: list of lane ids
        :return: The length of the vehicle in the lane.
        """
        try:all_len = self.lane_info[intersection_id][lanes_ids]['vehicle_length']
        except:all_len = [0]
        return all_len

    def get_vehicle_Gap_for_all_vehicals_in_lane(self,intersection_id,lanes_ids):
        """
        It returns a list of all the gaps between vehicles in a lane
        
        :param intersection_id: The id of the intersection
        :param lanes_ids: list of lane ids
        :return: The gap between the vehicle and the vehicle in front of it.
        """
        try:all_gap = self.lane_info[intersection_id][lanes_ids]['gap']
        except:all_gap = [0]
        return all_gap       

    #ANCHOR get_acceleration_for_all_vehicals_in_lanes
    def get_acceleration_for_all_vehicals_in_lane(self,intersection_id,lanes_ids):
        """
        It returns a list of all the acceleration values of all the vehicles in a lane
        
        :param intersection_id: The id of the intersection
        :param lanes_ids: list of lane ids
        :return: The acceleration of all vehicles in the lane.
        """
        try:all_acceleration = self.lane_info[intersection_id][lanes_ids]['vehicles_acceleration']
        except:all_acceleration = [0]
        return all_acceleration

    def get_number_of_vehical_for_all_neighbor_in_lane(self,intersection_id,lanes_ids):
        """
        It tries to get the number of vehicles in the lanes, but if it fails, it returns 0
        
        :param intersection_id: the id of the intersection
        :param lanes_ids: a list of lane ids
        :return: The number of vehicles in the lane.
        """
        try:all_number = self.get_num_veh_neighbor_lane(intersection_id,lanes_ids)
        except:all_number = 0
        return all_number

    def get_AvgSpeed_of_vehical_for_all_neighbor_lane(self,intersection_id,lanes_ids):
        """
        It takes in a list of lane ids and returns the average speed of vehicles in those lanes
        
        :param intersection_id: the id of the intersection
        :param lanes_ids: list of lane ids
        :return: The average speed of the vehicles in the neighboring lanes.
        """
        try:all_speed = self.get_avg_speed_veh_neighbor_lane(intersection_id,lanes_ids)
        except:all_speed = 0
        return all_speed

    def get_AvgAcceleration_of_vehical_for_all_neighbor_lane_in_lane(self,intersection_id,lanes_ids):
        """
        It returns the average acceleration of vehicles in the neighboring lanes of the lane.
        
        :param intersection_id: the id of the intersection
        :param lanes_ids: list of lane ids
        :return: The average acceleration of all vehicles in the neighboring lanes.
        """
        try:all_acceleration = self.get_avg_acceleration_veh_neighbor_lane(intersection_id,lanes_ids)
        except:all_acceleration = 0
        return all_acceleration

    def get_vehicle_arrangement_for_lane(self,intersection_id,lanes_ids):
        """
        It returns the vehicle arrangement for a given lane
        
        :param intersection_id: The id of the intersection
        :param lanes_ids: a list of lane ids
        :return: The vehicle arrangement for the lane.
        """
        try:arrangement = self.lane_info[intersection_id][lanes_ids]['vehicle_arrangement']
        except:arrangement = [0]
        return arrangement