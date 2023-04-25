from statistics import mean
import pandas as pd
import statistics
import datetime
import traci
import pytz

class SumoVariables:
    """
    class to store some variables in simulator
    """
    def __init__(self):
        self.avg_queue_lenght = 0
        self.speed_all_vehicles = []   
        self.count_vehicles = []     
        self.times = []
        self.queue_length = {'E1':[] , '-E2': [], 'E3':[],'-E4':[]}
        self.data_with_time = {}
    
    def get_vehicles_speed(self ,time ,  vehicles):
        """
        input:
        time: the current time
        vehicles: Vehicles whose speed I want to calculate
        """
        all_spd = []
        for i in range(0,len(vehicles)):

            spd = round(traci.vehicle.getSpeed(vehicles[i])*3.6,2)
            all_spd.append(spd)
            
        self.times.append(time)
        self.count_vehicles.append(len(vehicles))
        try:
            self.speed_all_vehicles.append(mean(all_spd))
        except statistics.StatisticsError:
            pass
        
    
    def store_queue_length(self,edge, queue_length):
        """
        input: 
        edge: id of edge
        queue_length: queue length
        
        this function will store that in list
        """
        # self.times.append(time)
        self.queue_length[edge].append(queue_length)
            

    def save_data_on_csv(self):
        """
        Generate Excel file contains all stored data

        """
        self.data_with_time = {'time' : self.times , 'avg_speed' : self.speed_all_vehicles ,
        'count_vehicles' : self.count_vehicles }
        # self.data_with_time[self.queue_length.keys(1)]

        dataset = pd.DataFrame(self.data_with_time, index=None)
        for key in self.queue_length.keys():
            dataset[key] = self.queue_length[key]
        dataset.to_csv("output_csv\\data_with_time.csv", index=False)