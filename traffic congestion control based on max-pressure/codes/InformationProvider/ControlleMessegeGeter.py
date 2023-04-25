from traci import trafficlight as t
from traci import vehicle as v
from traci import lane as l
import statistics
import sumolib
import time

class ControlleMessegeGeter:

    def __init__(self):    
        self.net = sumolib.net.readNet('Networks\\5-intersections\\5-intersections.net.xml')
        self.lane_state = {'G': 1,'g':1,'r':0,'y':2}
                
    def get_current_time(self):
        """
        This function returns the current time in seconds.
        :return: The current time in seconds.
        """
        start_time = time.time()
        return start_time

    def get_intersction_and_state(self,vehicle_id):
        """
        It returns the intersection id, state of the lane and whether the vehicle is in the controlled
        lane or not
        
        :param vehicle_id: The id of the vehicle
        :return: a tuple of three values:
        """
        nextTLS = v.getNextTLS(vehID=vehicle_id)
        if len(nextTLS) !=0 :
            intersection_id = nextTLS[0][0]
            state_of_lane = nextTLS[0][3]
            state_of_lane = self.lane_state[state_of_lane]
            controlled_lanes = t.getControlledLanes(intersection_id)
            is_add_vehicle = True if v.getLaneID(vehicle_id) in controlled_lanes else False
        else:
            is_add_vehicle = False
            intersection_id = None
            state_of_lane = None
        return is_add_vehicle,intersection_id,state_of_lane

    def get_position(self,vehicle_id):
        """
        It returns the position of the vehicle with the given vehicle_id
        
        :param vehicle_id: The ID of the vehicle to get the position of
        :return: The position of the vehicle.
        """
        return v.getPosition(vehicle_id)

    def get_speed(self,vehicle_id):
        """
        It returns the speed of a vehicle in km/h
        
        :param vehicle_id: The ID of the vehicle
        :return: The speed of the vehicle in km/h
        """
        return round(v.getSpeed(vehicle_id)*3.6,2)
    
    def get_acceleration(self,vehicle_id):
        """
        This function returns the acceleration of a vehicle
        
        :param vehicle_id: the id of the vehicle
        :return: The acceleration of the vehicle.
        """
        return v.getAcceleration(vehicle_id)

    def get_lane_id(self,vehicle_id):
        """
        > This function returns the lane ID of the vehicle with the given ID
        
        :param vehicle_id: the id of the vehicle
        :return: The lane ID of the vehicle.
        """
        return v.getLaneID(vehicle_id)
    
    def get_start_end_pos_lane(self,vehicle_id,by_vehicle=True):
        """
        It returns the start and end position of a lane
        
        :param vehicle_id: the id of the vehicle
        :param by_vehicle: if True, the vehicle_id is the vehicle id, if False, the vehicle_id is the
        lane id, defaults to True (optional)
        :return: The last and first element of the shape of the lane.
        """
        lane_id = self.get_lane_id(vehicle_id) if by_vehicle else vehicle_id
        shap_of_lane = l.getShape(lane_id)
        return shap_of_lane[-1] , shap_of_lane[0]
        
    def get_front_vehicle(self,vehicle_id):
        """
        If the vehicle has a leader, return the leader's ID. Otherwise, return -1
        
        :param vehicle_id: The ID of the vehicle for which we want to get the front vehicle
        :return: The vehicle ID of the front vehicle.
        """
        return v.getLeader(vehicle_id)[0] if v.getLeader(vehicle_id) != None else -1

    def lanes_leading(self,vehicle_id,by_vehicle=True):
        """
        > Given a vehicle id or a lane id, return the number of lanes leading to the given lane, and the
        ids of those lanes
        
        :param vehicle_id: the id of the vehicle you want to get the leading lanes of
        :param by_vehicle: if True, the vehicle_id is used to get the lane_id. If False, the vehicle_id
        is the lane_id, defaults to True (optional)
        :return: The number of lanes leading to the lane, the id of the first lane leading to the lane,
        and the id of the second lane leading to the lane.
        """
        lane_id = self.get_lane_id(vehicle_id) if by_vehicle else vehicle_id
        lane = self.net.getLane(lane_id)
        leading_lanes = lane.getIncoming()
        return len(leading_lanes), leading_lanes[0].getID() ,leading_lanes[1].getID() if len(leading_lanes)>1 else None
    
    def get_vehicle_length(self,vehicle_id):
        """
        It returns the length of the vehicle with the given id
        
        :param vehicle_id: the id of the vehicle
        :return: The length of the vehicle.
        """
        return v.getLength(vehicle_id)
    
    def get_gap(self,vehicle_id):
        """
        The function get_gap() returns the minimum gap between the vehicle with the given vehicle_id and the
        vehicle in front of it
        
        :param vehicle_id: the id of the vehicle
        :return: The minimum gap between the vehicle and the vehicle in front of it.
        """
        return v.getMinGap(vehicle_id)

    def get_turning_angle(self,vehicle_id):
        """
        This function returns the turning angle of the vehicle
        
        :param vehicle_id: The ID of the vehicle
        :return: The angle of the vehicle.
        """
        return round(v.getAngle(vehicle_id),2)

    def get_vehicle_arrangement(self,vehicle_id,by_vehicle=True):
        """
        > The function returns the position of the vehicle in the lane
        
        :param vehicle_id: the id of the vehicle you want to get the position of
        :param by_vehicle: if True, the vehicle_id is used to find the lane_id. If False, the lane_id is
        used directly, defaults to True (optional)
        :return: The index of the vehicle in the lane.
        """
        lane_id = self.get_lane_id(vehicle_id) if by_vehicle else vehicle_id
        id_veh_in_lane = list(l.getLastStepVehicleIDs(lane_id))
        id_veh_in_lane.reverse()
        return id_veh_in_lane.index(vehicle_id)

    def get_lane_length(self,vehicle_id,by_vehicle=True):
        """
        > Get the length of a lane
        
        :param vehicle_id: the id of the vehicle
        :param by_vehicle: if True, the vehicle_id is used to get the lane_id. If False, the vehicle_id
        is the lane_id, defaults to True (optional)
        :return: The length of the lane.
        """
        lane_id = self.get_lane_id(vehicle_id) if by_vehicle else vehicle_id
        return l.getLength(lane_id)

    def get_number_of_vehical_on_lane(self,vehicle_id,by_vehicle=True):
        """
        It returns the number of vehicles on a lane
        
        :param vehicle_id: The id of the vehicle you want to get the lane id of
        :param by_vehicle: if True, the vehicle_id is the vehicle's id, if False, the vehicle_id is the
        lane's id, defaults to True (optional)
        :return: The number of vehicles on the lane.
        """
        lane_id = self.get_lane_id(vehicle_id) if by_vehicle else vehicle_id
        return l.getLastStepVehicleNumber(lane_id)

    def get_number_of_places_available_in_lane(self,vehicle_id,by_vehicle=True):
        """
        It returns the number of places available in a lane, given the vehicle id
        
        :param vehicle_id: The id of the vehicle you want to get the number of places available for
        :param by_vehicle: if True, then the vehicle_id is the vehicle id, if False, then the vehicle_id
        is the lane id, defaults to True (optional)
        :return: The number of places available in the lane.
        """
        lane_id = self.get_lane_id(vehicle_id) if by_vehicle else vehicle_id
        mean_length_veh = l.getLastStepLength(lane_id)
        count_veh = self.get_number_of_vehical_on_lane(lane_id,by_vehicle=False)
        return (self.get_lane_length(vehicle_id)-( count_veh*(mean_length_veh+self.get_gap(vehicle_id))))//(mean_length_veh+self.get_gap(vehicle_id))
    
    def get_information_for_neighbor_lane(self,vehicle_id,by_vehicle=True):
        if by_vehicle:
            _ , lane_leading_r , _ = self.lanes_leading(vehicle_id)
        else:
            lane_id = self.get_lane_id(vehicle_id) 
            _ , lane_leading_r , _ = self.lanes_leading(lane_id)
        num_veh_neighbor_lane =  self.get_number_of_vehical_on_lane(lane_leading_r,by_vehicle=False)
        avg_speed_veh_neighbor_lane = l.getLastStepMeanSpeed(lane_leading_r) if num_veh_neighbor_lane>0 else 0
        ids_vehicle_on_lane_neighbor = l.getLastStepVehicleIDs(lane_leading_r)
        accelerations = []
        avg_acceleration_veh_neighbor_lane = 0
        for id in ids_vehicle_on_lane_neighbor:
            accelerations.append(v.getAcceleration(id))
        try:
            avg_acceleration_veh_neighbor_lane = statistics.mean(accelerations)
        except:
            statistics.StatisticsError
            pass

        return num_veh_neighbor_lane,avg_speed_veh_neighbor_lane,avg_acceleration_veh_neighbor_lane
    
    def get_lane_info(self,vehicles):
        """        
        :param vehicles: list of vehicles
        :return: a dictionary of dictionaries. The first dictionary has the intersection id as the key
        and the second dictionary has the lane id as the key. The second dictionary has the following
        keys:
        """
        lane_info = {}
        for i in range(0,len(vehicles)):
            is_add_vehicle,intersection_id,state_of_lane = self.get_intersction_and_state(vehicles[i])
            if is_add_vehicle:
                if not intersection_id in  lane_info:
                    lane_info[intersection_id] = {}
                lane_id = self.get_lane_id(vehicles[i])
                if not lane_id in lane_info[intersection_id]:
                    lane_info[intersection_id][lane_id] = {}
                    lane_info[intersection_id][lane_id]['Times_send'] = []
                    lane_info[intersection_id][lane_id]['vehicles_speed'] = []
                    lane_info[intersection_id][lane_id]['vehicles_acceleration'] = []
                    lane_info[intersection_id][lane_id]['X_position'] = []
                    lane_info[intersection_id][lane_id]['Y_position'] = []
                    lane_info[intersection_id][lane_id]['front_vehicle'] = []
                    lane_info[intersection_id][lane_id]['vehicle_length'] = []
                    lane_info[intersection_id][lane_id]['gap'] = []
                    lane_info[intersection_id][lane_id]['vehicle_arrangement'] = []
                    lane_info[intersection_id][lane_id]['turning_angle'] = []
                    lane_info[intersection_id][lane_id]["state"] = state_of_lane
                    lane_info[intersection_id][lane_id]['Angle'] = self.get_turning_angle(vehicles[i])
                    lane_info[intersection_id][lane_id]['start_point'],lane_info[intersection_id][lane_id]['end_point'] = self.get_start_end_pos_lane(lane_id,by_vehicle=False)
                    _,lane_info[intersection_id][lane_id]['right_leading_lane'],lane_info[intersection_id][lane_id]['straight_leading_lane'] = self.lanes_leading(lane_id,by_vehicle=False)
                    lane_info[intersection_id][lane_id]['lane_length'] = self.get_lane_length(lane_id,by_vehicle=False)
                    lane_info[intersection_id][lane_id]['number_of_vehical'] = self.get_number_of_vehical_on_lane(lane_id,by_vehicle=False)
                    lane_info[intersection_id][lane_id]['number_of_places_available'] = self.get_number_of_places_available_in_lane(vehicles[i],by_vehicle=True)
                    lane_info[intersection_id][lane_id]['num_veh_neighbor_lane'],lane_info[intersection_id][lane_id]['avg_speed_veh_neighbor_lane'],lane_info[intersection_id][lane_id]['avg_acceleration_veh_neighbor_lane'] = self.get_information_for_neighbor_lane(vehicles[i],by_vehicle=True)
                    lane_info[intersection_id][lane_id]['number_of_vehicles_moving_from_straight_lane'] = self.get_number_of_vehical_on_lane(lane_info[intersection_id][lane_id]['straight_leading_lane'],by_vehicle=False)
                    lane_info[intersection_id][lane_id]['number_of_vehicles_moving_from_right_lane'] = self.get_number_of_vehical_on_lane(lane_info[intersection_id][lane_id]['right_leading_lane'],by_vehicle=False)
                lane_info[intersection_id][lane_id]['Times_send'].append(self.get_current_time())    
                lane_info[intersection_id][lane_id]['vehicles_speed'].append(self.get_speed(vehicles[i]))
                lane_info[intersection_id][lane_id]['vehicles_acceleration'].append(self.get_acceleration(vehicles[i]))
                X,Y = self.get_position(vehicles[i])
                lane_info[intersection_id][lane_id]['X_position'].append(X)
                lane_info[intersection_id][lane_id]['Y_position'].append(Y)
                lane_info[intersection_id][lane_id]['front_vehicle'].append(self.get_front_vehicle(vehicles[i]))
                lane_info[intersection_id][lane_id]['vehicle_length'].append(self.get_vehicle_length(vehicles[i]))
                lane_info[intersection_id][lane_id]['gap'].append(self.get_gap(vehicles[i]))
                lane_info[intersection_id][lane_id]['vehicle_arrangement'].append(self.get_vehicle_arrangement(vehicles[i]))
                lane_info[intersection_id][lane_id]['turning_angle'].append(self.get_turning_angle(vehicles[i]))
        return lane_info
