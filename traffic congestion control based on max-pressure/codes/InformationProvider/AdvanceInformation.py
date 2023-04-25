import numpy as np

class AdvanceInformation:
    def __init__(self,infromation_converter):
        self.infromation_converter = infromation_converter



    def get_reward_info(self,lane_info,intersection_id):
        """
        It takes in the lane_info and intersection_id and returns a list of lists. Each list contains
        the number of vehicles in the lane, the number of places available in the lane, the number of
        vehicles in the right and straight leading lanes, and the state of the right and straight
        leading lanes
        
        :param lane_info: the information of the lanes
        :param intersection_id: the id of the intersection
        :return: a list of lists. Each list contains the following information:
        """
        self.infromation_converter.setattr(lane_info)
        reward_info = []
        lanes = self.infromation_converter.get_lanes_in_intersction(intersection_id)
        for lane_id in lanes:
            temp = []
            temp.append(self.infromation_converter.get_number_of_vehical(intersection_id,lane_id))
            temp.append(self.infromation_converter.get_number_of_places_available(intersection_id,lane_id))
            R,S = self.infromation_converter.get_right_leading_lane(intersection_id,lane_id),self.infromation_converter.get_straight_leading_lane(intersection_id,lane_id)
            temp.append([self.infromation_converter.get_number_of_v(R),self.infromation_converter.get_number_of_v(S)])
            temp.append([self.infromation_converter.get_lane_state(R),self.infromation_converter.get_lane_state(S)])
            reward_info.append(temp)
        return reward_info
    
    def get_state_info(self,lane_info,intersection_id):
        """
        It takes in a lane_info object and an intersection_id and returns a list of lists of information
        about the lanes in the intersection
        
        :param lane_info: the information of the lanes in the intersection
        :param intersection_id: The id of the intersection
        :return: a list of lists. Each list contains the following information:
        """
        self.infromation_converter.setattr(lane_info)
        lanes = self.infromation_converter.get_lanes_in_intersction(intersection_id)
        state_info = []
        for _,lane in enumerate(lanes):
            vehicles_arrangement = self.infromation_converter.get_vehicle_arrangement_for_lane(intersection_id,lane)
            copy_vehicles_arrangement = vehicles_arrangement.copy()
            copy_vehicles_arrangement.sort()
            index = []
            for _,vehicle_arrangement in enumerate(copy_vehicles_arrangement):
                index.append(vehicles_arrangement.index(vehicle_arrangement))
            x_pos_vehicals = np.array(self.infromation_converter.get_Xposition_for_all_vehicals_in_lane(intersection_id,lane))
            x_pos_vehicals = x_pos_vehicals[index].tolist()
            y_pos_vehicals = np.array(self.infromation_converter.get_Yposition_for_all_vehicals_in_lane(intersection_id,lane))[index].tolist()
            length_lane = self.infromation_converter.get_lane_length(intersection_id,lane)
            s_p = self.infromation_converter.get_start_lane(intersection_id,lane)
            x_start_lane,y_start_lane = s_p[0],s_p[1]
            e_p = self.infromation_converter.get_end_lane(intersection_id,lane)
            x_end_lane,y_end_lane = e_p[0],e_p[1]
            lane_angel = self.infromation_converter.get_Angle(intersection_id,lane)
            vehicles_arrangement_ = copy_vehicles_arrangement
            State_signal = self.infromation_converter.get_state(intersection_id,lane)
            Time_sent = np.array(self.infromation_converter.get_time_send_for_all_vehicals_in_lane(intersection_id,lane))[index].tolist()
            Speed_sent = np.array(self.infromation_converter.get_speed_for_all_vehicals_in_lane(intersection_id,lane))[index].tolist()
            vehicle_length = np.array(self.infromation_converter.get_vehicle_length_for_all_vehicals_in_lane(intersection_id,lane))[index].tolist()
            Gap = np.array(self.infromation_converter.get_vehicle_Gap_for_all_vehicals_in_lane(intersection_id,lane))[index].tolist()
            acceleration = np.array(self.infromation_converter.get_acceleration_for_all_vehicals_in_lane(intersection_id,lane))[index].tolist()
            number_neighbor = self.infromation_converter.get_number_of_vehical_for_all_neighbor_in_lane(intersection_id,lane)
            speed_neighbor = self.infromation_converter.get_AvgSpeed_of_vehical_for_all_neighbor_lane(intersection_id,lane)
            acc_neighbor = self.infromation_converter.get_AvgAcceleration_of_vehical_for_all_neighbor_lane_in_lane(intersection_id,lane)
            state_info.append([x_pos_vehicals,y_pos_vehicals,length_lane,x_start_lane,y_start_lane,
            x_end_lane,y_end_lane,lane_angel,vehicles_arrangement_,State_signal,Time_sent,Speed_sent,vehicle_length,Gap,acceleration,number_neighbor,speed_neighbor,acc_neighbor])
        return state_info