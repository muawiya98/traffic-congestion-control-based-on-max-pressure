import os
import sys
sys.path.append(os.path.abspath("."))
from codes.Environment.configuration import Network
from codes.RL_Algo.Controller import Controller
from traci import trafficlight as t
from sumolib import checkBinary
from traci import start
import optparse
import traci


class SUMO_ENV:

    def __init__(self,time = 1000 , number_cars_mean_std ={'loc':15 , 'scale':4} ,period_of_generation_mean = 2 , is_random_routes = False):
        self.period_of_generation_mean = period_of_generation_mean
        self.number_cars_mean_std = number_cars_mean_std
        self.is_random_routes = is_random_routes
        self.time = time

        
    def get_options(self):
        """
        The function get_options() is used to parse the command line arguments
        :return: The options and arguments are being returned.
        """
        opt_parser = optparse.OptionParser()
        opt_parser.add_option("--nogui", action="store_true",
                            default=False, help="run the commandline version of sumo")
        options, _ = opt_parser.parse_args()
        return options
    
    def starting(self):
        """
        The function starts the simulation by calling the sumoBinary, which is the sumo-gui or sumo
        depending on the nogui option
        """
        if self.get_options().nogui:
            sumoBinary = checkBinary('sumo')
        else:
            sumoBinary = checkBinary('sumo-gui')
        start([sumoBinary, "-c", Network['network']])
    
    def exit(self):
        """
        The function is called when the simulation is ended
        """
        traci.close()
        sys.stdout.flush()
    
    def run(self):
        """
        The function runs the simulation 5 times, each time with a different set of parameters
        """
        for i in range(5):
            self.starting()
            self.intersection = t.getIDList()
            self.controller = Controller(self.intersection,self.time,self.number_cars_mean_std,self.period_of_generation_mean,self.is_random_routes)
            # Normal scenario
            if i ==0:self.controller.run_agents(Random=False,with_agents=True,with_predicted_position=True,without_restart=False)
            # Run RL algorithm without regard for the delay 
            elif i ==1:self.controller.run_agents(Random=False,with_agents=True,with_predicted_position=False,without_restart=False)
            # Rely on sumo decisions
            elif i ==2:self.controller.run_agents(Random=False,with_agents=False,with_predicted_position=False,without_restart=False)
            # Give a random action
            elif i ==3:self.controller.run_agents(Random=True,with_agents=False,with_predicted_position=False,without_restart=False)
            # without restart 
            elif i==4:self.controller.run_agents(Random=False,with_agents=True,with_predicted_position=True,without_restart=True)
            self.exit()

# A way to run the code only if the file is run directly.
if __name__ == "__main__" :
    env = SUMO_ENV(time = Network['time'],number_cars_mean_std= Network['number_cars_mean_std'],
        period_of_generation_mean = Network['period_of_generation_mean'],
        is_random_routes= False)
    env.run()
    
    # try:
    #     env.run()
    # except:
    #     print("there are an error")
