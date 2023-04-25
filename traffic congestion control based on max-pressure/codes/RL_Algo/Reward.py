class Reward:        
    def calculate_pressure_of_vehicular_movement(self,numberOfVehicles_l_m,C,trafficSignals,numberOfVehicles_k_l) :
        """
        It calculates the pressure of vehicular movement
        
        :param numberOfVehicles_l_m: number of vehicles in the link
        :param C: is the capacity of the road
        :param trafficSignals: a list of traffic signal times for each intersection
        :param numberOfVehicles_k_l: is a list of the number of vehicles in each lane
        """
        T = 0 
        for i,trafficsignal in enumerate(trafficSignals):
            T += trafficsignal*numberOfVehicles_k_l[i]
            
        return numberOfVehicles_l_m - C + T
    
    def pressure_on_intersection(self,LANES): # (3) 5
        """
        It calculates the pressure of the intersection by adding the pressure of each lane
        
        :param LANES: a list of tuples, each tuple containing the following:
        :return: The pressure of the intersection.
        """
        pressureOfIntersection = 0
        for lane in LANES:
            pressureOfIntersection += self.calculate_pressure_of_vehicular_movement(lane[0],lane[1],lane[2],lane[3])
        return pressureOfIntersection
    
    def reward(self,LANES): # (4) 5
        """
        > The reward function is the negative of the pressure on the intersection
        
        :param LANES: the number of lanes in the intersection
        :return: The reward is the negative of the pressure on the intersection.
        """
        return -self.pressure_on_intersection(LANES)