# from plistlib import UID
from codes.Environment.traffic_lights_controler import traffic_lights_controler
from codes.Environment.configuration import Vehicle_characteristics,Network
from codes.InformationProvider.ControlleMessegeGeter import ControlleMessegeGeter
from codes.InformationProvider.InformationConverter import InfromationConverter
from codes.InformationProvider.AdvanceInformation import AdvanceInformation
from codes.Environment.traffic_light_signal import traffic_light
from codes.RL_Algo.Reward import Reward
from codes.RL_Algo.State import State
from codes.RL_Algo.Agent import Agent
import matplotlib.pyplot as plt # type: ignore
from traci import vehicle as v
from numpy import concatenate
from traci import lane as l
from statistics import mean
import statistics
from numpy import random # type: ignore 
from uuid import uuid4
import traci
import os




class Controller():
    def __init__(self,intersection,time,number_cars_mean_std,period_of_generation_mean,is_random_routes,max_len_queue=1000):
        self.period_of_generation_mean = period_of_generation_mean
        self.controlle_messege_geter = ControlleMessegeGeter()
        self.infromationConverter = InfromationConverter(self.controlle_messege_geter)
        self.advanceInformation  = AdvanceInformation(self.infromationConverter)
        self.number_cars_mean_std = number_cars_mean_std
        self.is_random_routes = is_random_routes
        self.number_of_agent = len(intersection)
        self.Agent_ids = intersection
        self.reward = Reward()
        self.state = State()
        self.Agents = []
        self.memory = {}
        self.averag_queue_length = []
        self.average_waiting_time = []
        self.std_waiting_time = []
        self.time = time
        self.num = 200
    
    def get_all_edges(self):
        """
        It returns a list of all the edges in the network
        :return: A list of all the edges in the network.
        """
        opjects,all_edges = traci.edge.getIDList(),[]
        for obj in opjects:
            if 'E' in(obj):
                all_edges.append(obj)
        return all_edges
    
    def get_edges_ignored(self):
        """
        It takes all the edges in the network and compares them to the edges controlled by the traffic
        lights. 
        
        The edges controlled by the traffic lights are the ones that are returned. 
        
        The edges that are not controlled by the traffic lights are ignored. 
        
        The edges that are ignored are the ones that are returned. 
        
        The edges that are controlled by the traffic lights are ignored. 
        
        The edges that are ignored are the ones that are returned. 
        
        The edges that are controlled by the traffic lights are ignored. 
        
        The edges that are ignored are the ones that are returned. 
        
        The edges that are controlled by the traffic lights are ignored. 
        
        The edges that are ignored are the ones that are returned. 
        
        The edges that are controlled by the traffic lights are ignored. 
        
        The edges that are ignored are the ones that are returned. 
        
        The edges that are controlled by
        :return: Edges_controlled is a list of edges that are controlled by the traffic light.
        Edges_non_controlled is a list of edges that are not controlled by the traffic light.
        """
        all_edges = self.get_all_edges()
        lanes_controlled = []
        for id_tl in self.Agent_ids:lanes_controlled.extend(traci.trafficlight.getControlledLanes(id_tl)) # type: ignore
        Edges_controlled = []
        Edges_non_controlled = []
        for Ei in all_edges:
            for Li in lanes_controlled:
                if Ei in Li:
                    if Ei == 'E18' or Ei == 'E22': pass
                    else:Edges_controlled.append(Ei)
                # else:Edges_non_controlled.append(Ei)
        set1 = set(all_edges)
        set2 = set(Edges_controlled)
        non_controlled = set1.difference(set2).union(set2.difference(set1))

        Edges_controlled = list(set(Edges_controlled))
        # Edges_non_controlled = list(set(Edges_non_controlled))
        Edges_non_controlled = list(non_controlled)
        return Edges_controlled , Edges_non_controlled
    
    
    def generate_vehicles_(self,number_vehicles,all_edges,step):
        """
        It generates vehicles with random routes and adds them to the simulation
        
        :param number_vehicles: number of vehicles to be generated
        :param all_edges: list of all edges in the network
        :param step: the current step of the simulation
        """
        for i in range(number_vehicles):
            routes = traci.route.getIDList()
            if (self.is_random_routes):
                v.add(vehID = 'Veh'+str(step)+str(i), routeID = random.choice(routes))
            else:
                edge1,edge2,uid = random.choice(all_edges),random.choice(all_edges),str(uuid4())
                traci.route.add(routeID= uid , edges= [edge1,edge2] )
                v.add(vehID = 'Veh'+uid, routeID = uid)
            v.setLength('Veh'+uid , Vehicle_characteristics['length'])  # type: ignore
            v.setMinGap('Veh'+uid , Vehicle_characteristics['min_cap'])  # type: ignore

    def generate_vehicles(self,number_vehicles,edge_non_contlled,Edges_controlled):
        """
        It generates a random route for each vehicle and adds it to the simulation
        
        :param number_vehicles: number of vehicles to be generated
        :param all_edges: list of all edges in the network
        """
        for i in range(number_vehicles):     
            routes = traci.route.getIDList()
            edge1 = random.choice(Edges_controlled)
            edge2 = random.choice(edge_non_contlled)
            
            uid = str(uuid4())
            traci.route.add(routeID= uid , edges= [edge1,edge2] )
            
            traci.vehicle.add(vehID = 'Veh'+uid, routeID = uid)
            traci.vehicle.setLength('Veh'+uid , Vehicle_characteristics['length'])
            traci.vehicle.setMinGap('Veh'+uid , Vehicle_characteristics['min_cap'])

    def set_vehicle_info(self,step,all_edges,period_of_generation,is_generate,edge_non_contlled,Edges_controlled):
        """
        > The function generates a number of vehicles according to a normal distribution with mean and
        standard deviation specified in the `number_cars_mean_std` dictionary. The number of vehicles is
        generated every `period_of_generation_mean` seconds
        
        :param step: the current step of the simulation
        :param all_edges: a list of all the edges in the network
        :param period_of_generation: This is the period of time between the generation of vehicles
        :param is_generate: a boolean that tells us whether we should generate vehicles or not
        :return: period_of_generation,is_generate
        """
        if period_of_generation == 0:
            is_generate,period_of_generation = True,int(random.exponential(scale = self.period_of_generation_mean))
        period_of_generation-=1 if period_of_generation>0 else 0
        if is_generate:
            is_generate = False 
            number_vehicles = int(random.normal(loc=self.number_cars_mean_std['loc'] , scale= self.number_cars_mean_std['scale']))
            self.generate_vehicles(number_vehicles,edge_non_contlled,Edges_controlled)
        return period_of_generation,is_generate

    def creator(self):
        """
        It creates a list of agents, each with a unique ID, and appends them to the Agents list.
        """
        for i in range(self.number_of_agent):
            self.Agents.append(Agent(self.Agent_ids[i]))
        
    def save_strat_state(self):
        """
        The function saves the current simulation state to a file called 'start_state.xml' in the same
        directory as the network file
        """
        path_start_state =  Network['network']
        path_0 = path_start_state.split('.')[0]
        path_start_state = path_0+'_start_state.xml'
        traci.simulation.saveState(path_start_state)

    def load_strat_state(self):
        """
        It loads a saved simulation state
        """
        ###  get path of 'start state' #### 
        path_start_state =  Network['network']
        path_0 = path_start_state.split('.')[0]
        path_start_state = path_0+'_start_state.xml'
        # load a saved simulation state
        traci.simulation.loadState(path_start_state)

    def check_vehicles_to_remove(self, edges):
        """
        It removes all vehicles from the given edges
        
        :param edges: list of edges to remove vehicles from
        """
        # def remove_vehicles(vehicles):
        #     map(lambda veh: traci.vehicle.remove(veh), vehicles)
        
        # map(lambda edge: remove_vehicles(traci.edge.getLastStepVehicleIDs(edge)), edges)
        
        for id_Edge in edges:
            vehicle_ids = traci.edge.getLastStepVehicleIDs(id_Edge)
            for id_vehicle in vehicle_ids:
                traci.vehicle.remove(id_vehicle)
    
    def rest_sumo(self):
        """
        The function is called by the main function, and it calls the plot_reward function of each agent
        
        :param number_of_senareo: number of episodes
        """
        self.load_strat_state()
    
    def maping_btween_agents_intersections(self):
        """
        It creates a traffic light object for each agent, and then creates a traffic lights controller
        object
        :return: a tuple of three objects.
        """
        t_obejct,Actions = [],{}
        for id in self.Agent_ids:
            t_obejct.append(traffic_light(id))
            Actions[id] = (0,1)
        tls_controler = traffic_lights_controler(t_obejct)
        return t_obejct,Actions,tls_controler

    def functionality_agents(self,lane_information,actions,with_predicted_position):
        """
        It takes in the lane information, the actions, and a boolean value, and returns the state,
        action, and actions
        
        :param lane_information: a dictionary of the form {agent_id: [agent_x, agent_y, agent_vx,
        agent_vy, agent_speed, agent_lane, agent_s, agent_d]}
        :param actions: a dictionary of actions for each agent
        :param with_predicted_position: This is a boolean value that determines whether the agent will
        be given the predicted position of the other agents in the environment
        :return: The state, action, and actions are being returned.
        """
        state,action = [],[]
        for i,id in enumerate(self.Agent_ids):
            state.append(self.state.state(self.advanceInformation.get_state_info(lane_information,id),with_predicted_position))
            ac = self.Agents[i].get_action(state[i])
            ac = (int(ac[0]),int(ac[1]))
            actions[id] = ac
            action.append(list(actions[id]))
        return state,action,actions
    
    def apply_action(self,with_agents,tls_controler,t_obejct,actions):
        """
        It takes in a list of agents, a traffic light controller, a list of traffic light objects, and a
        dictionary of actions. 
        
        If the with_agents flag is set to true, it sends the actions to the traffic light controller. 
        
        If the with_agents flag is set to false, it randomly generates actions for each agent and sends
        them to the traffic light controller. 
        
        Then, it checks the commands to execute for each agent.
        
        :param with_agents: whether to use the agent or not
        :param tls_controler: the traffic light controller
        :param t_obejct: a list of traci objects
        :param actions: a dictionary of actions for each agent
        """
        if with_agents:
            tls_controler.send_Actions(actions)
        else:
            actions={}
            for i,id in enumerate(self.Agent_ids):
                temp = random.choice([0, 1])
                actions[id] = (temp,1-temp)
            tls_controler.send_Actions(actions)
        for i,id in enumerate(self.Agent_ids):
            t_obejct[i].check_cmds_to_execute()


    
    def calculate_reward_and_train_DQN(self,lane_info,state_saver,action_saver,with_agents):
        """
        It calculates the reward for each agent and trains the DQN for each agent
        
        :param lane_info: a list of lane information, which is a list of the following format:
        :param state_saver: a list of lists of the current state of each agent
        :param action_saver: a list of actions that the agents took in the previous step
        :param t_obejct: a list of objects that are used to control the agents
        :param with_agents: boolean, whether to train the agent or not
        """
        if with_agents:
            current_state,next_state,current_action = state_saver[0],state_saver[1],action_saver[0]
        for i,id in enumerate(self.Agent_ids):
            reward = self.reward.reward(self.advanceInformation.get_reward_info(lane_info,id))
            self.Agents[i].rewards.append(reward)
            if with_agents:
                self.Agents[i].replay_bufer(current_state[i],current_action[i],reward,next_state[i])  # type: ignore
                
    
    def calculate_queue_length(self,lane_ids):
        """
        queuq length refers to the number of vehicles waiting on one side of the road 
        """
        AQL = []
        for lane_id in lane_ids:
            count_veh = l.getLastStepHaltingNumber(lane_id)
            length_lane = l.getLength(lane_id)
            AQL.append(count_veh*7.5 / length_lane)
        return mean(AQL)
    
    def get_list_of_waiting_vehicles(self , vehicles):
        """
        It takes a list of vehicles and returns a list of waiting times for each vehicle in the list
        
        :param vehicles: list of vehicles
        :return: The waiting time of the vehicles in the list.
        """
        # apply a function to all values in the list using map and lambda
        waiting_time_vehicles = list(map(lambda veh: traci.vehicle.getWaitingTime(veh), vehicles))
        return waiting_time_vehicles
    
    def get_average_waiting_time_overall(self,vehicles):
        """
        It returns the average waiting time of all vehicles in the simulation
        
        :param vehicles: list of vehicles
        :return: The average waiting time of all vehicles in the simulation.
        """
        if len(vehicles)>0:
            waiting_time_vehicles = self.get_list_of_waiting_vehicles(vehicles)
            average = sum(waiting_time_vehicles) / len(waiting_time_vehicles)
            return average
        else:
            return -1
    
    def get_std_waiting_time_overall(self,vehicles):
        """
        It takes a list of vehicles and returns the standard deviation of the waiting time of all
        vehicles in the list
        
        :param vehicles: list of vehicles
        :return: The standard deviation of the waiting time of all vehicles in the simulation.
        """
        if len(vehicles)>0:
            waiting_time_vehicles = self.get_list_of_waiting_vehicles(vehicles)
            std_dev = statistics.stdev(waiting_time_vehicles)
            return std_dev
        else:
            return -99999
    
    def run_agents(self,Random,with_agents,with_predicted_position,without_restart):
        """
        The function runs the simulation for a given number of steps, and at each step it checks if the
        number of vehicles is less than the number of vehicles that should be in the simulation, and if
        so, it generates more vehicles
        
        :param Random: If True, the agent will not be used and the traffic lights will be controlled
        randomly
        :param with_agents: True if you want to use the agents, False if you want to use the DQN
        :param with_predicted_position: If True, the agent will use the predicted position of the
        vehicle to make a decision
        :param without_restart: if True, the simulation will not be restarted after 3000 steps
        """
        self.creator()
        state_saver,action_saver,step_generation,step,period_of_generation,is_generate = [],[],0,0,0,False
        t_obejct,Actions,tls_controler = self.maping_btween_agents_intersections()
        # all_edges = self.get_all_edges()
        Edges_controlled,edge_non_contlled = self.get_edges_ignored()
        while step < self.time:
            self.check_vehicles_to_remove(edge_non_contlled)
            traci.simulationStep()
            if step == 0:self.save_strat_state()
            if step_generation == 0:self.generate_vehicles(self.num+self.num//3,edge_non_contlled,Edges_controlled)  
            if step % 30 == 0: #and step != 0 :
                vehicles = v.getIDList()
                lane_info = self.controlle_messege_geter.get_lane_info(vehicles)
                if with_agents:
                    state,action,Actions = self.functionality_agents(lane_info,Actions,with_predicted_position)
                    state_saver.append(state)
                    action_saver.append(action)
                    self.apply_action(with_agents,tls_controler,t_obejct,Actions)
                    if len(state_saver)>1:
                        self.calculate_reward_and_train_DQN(lane_info,state_saver,action_saver,with_agents)
                        action_saver.pop(0)
                        state_saver.pop(0)
                elif Random:
                    self.apply_action(with_agents,tls_controler,t_obejct,Actions)
                    self.calculate_reward_and_train_DQN(lane_info,state_saver,action_saver,with_agents)
                else:
                    self.calculate_reward_and_train_DQN(lane_info,state_saver,action_saver,with_agents)
                lane_ids = concatenate([self.infromationConverter.get_lanes_in_intersction(i) for i in self.Agent_ids])
                if step % 3000 != 0 and step!=0 :
                    self.averag_queue_length.append(self.calculate_queue_length(lane_ids))
                    self.average_waiting_time.append(self.get_average_waiting_time_overall(vehicles))
                    self.std_waiting_time.append(self.get_std_waiting_time_overall(vehicles))

            if step_generation> 30 and len(v.getIDList()) <self.num:
                number_cars = self.num - len(v.getIDList())
                self.generate_vehicles(number_cars,edge_non_contlled,Edges_controlled) 
            step_generation +=1
            if step % 3000 == 0 and step != 0:
                if not without_restart:
                    self.rest_sumo()
                    step_generation = 0 
            # period_of_generation,is_generate = self.set_vehicle_info(step,all_edges,period_of_generation,is_generate,edge_non_contlled,Edges_controlled)
            step += 1
        self.polt_all_results(Random,with_agents,with_predicted_position,without_restart)

    def polt_all_results(self,Random,with_agents,with_predicted_position,without_restart):
        """
        It plots the results of the simulation
        
        :param Random: If True, the agents will be randomly placed in the environment. If False, the
        agents will be placed in a grid
        :param with_agents: If True, the plot will show the agents' positions
        :param with_predicted_position: If True, the agent will use the predicted position of the other
        agents to make its decision. If False, the agent will use the actual position of the other
        agents to make its decision
        :param without_restart: If you want to plot the results of the simulation without restarting the
        simulation, set this parameter to True
        """
        for i in range(self.number_of_agent,):
            self.Agents[i].plot_reward(with_agents,with_predicted_position,Random,without_restart)
        
        self.plot_result(self.averag_queue_length,"Averag_Queue_Length",Random,with_agents,with_predicted_position,without_restart) 
        self.plot_result(self.average_waiting_time,"Average_Waiting_Time",Random,with_agents,with_predicted_position,without_restart)
        self.plot_result(self.std_waiting_time,"STD_Waiting_Time",Random,with_agents,with_predicted_position,without_restart)
        

    
    def plot_result(self,List_of_value,title,Random,with_agents,with_predicted_position,without_restart,step=5):
        """
        It takes a list of values, a title, a boolean for whether or not the results are random, a
        boolean for whether or not the results are with agents, a boolean for whether or not the results
        are with predicted positions, a boolean for whether or not the results are without restart, and
        a step value. 
        
        It then plots the list of values, with the title, and saves the plot to a file. 
        
        The file is saved to a folder called "results" in the current directory, and the folder name is
        determined by the booleans. 
        
        The step value is used to determine how many values to plot. 
        
        The function also plots vertical lines at every 100th step. 
        
        The function also prints the path to the file that it saves the plot to. 
        
        The function also has a commented out line that shows the plot.
        
        :param List_of_value: the list of values you want to plot
        :param title: The title of the graph
        :param Random: If True, the agents will be randomly placed on the grid. If False, the agents
        will be placed in a circle
        :param with_agents: whether or not to use the agents
        :param with_predicted_position: If True, the agents will use the predicted position of the other
        agents to make their decisions. If False, they will use the actual position of the other agents
        :param without_restart: if True, the agent will not restart when it reaches the goal
        :param step: the number of steps between each point plotted, defaults to 5 (optional)
        """
        plt.figure(figsize=(6, 4))
        plt.title(title)
        plt.plot([i for i, x in enumerate(List_of_value) if i%step==0],
                 [x for i, x in enumerate(List_of_value) if i%step==0], color='g')
        n = len(List_of_value)
        plt.vlines(x=[i for i in range(n) if i%100==0], ymin=[min(List_of_value) for i in range(n) if i%100==0], ymax=[max(List_of_value) for i in range(n) if i%100==0], colors=['r' for i in range(n) if i%100==0], ls='--', lw=2)
        
        plt.xlabel('Steps')
        plt.ylabel(title)
        folder_name = ""
        if with_agents and with_predicted_position:folder_name = "Results_with_predicted_position"
        elif with_agents and not with_predicted_position:folder_name = "Results_without_predicted_position"
        elif not with_agents and not with_predicted_position:folder_name = "Results_without_agents"
        if Random : folder_name = "Results_Random"
        if without_restart:folder_name = "Results_without_restart"
        print(os.path.join(os.path.join(os.path.join(os.path.abspath("."),'resultes'),folder_name),folder_name+"_"+title+".png"))
        plt.savefig(os.path.join(os.path.join(os.path.join(os.path.abspath("."),'resultes'),folder_name),title+".png"))
        # plt.show()
        
        

    