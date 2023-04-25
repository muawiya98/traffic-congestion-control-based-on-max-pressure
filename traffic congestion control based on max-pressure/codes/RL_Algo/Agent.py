from codes.RL_Algo.DQN import DQN
import matplotlib.pyplot as plt
from collections import deque
import sys
import os

class Agent:
    def __init__(self,agent_id,batch_size=16,max_len_queue=10000):
        self.agent_id = agent_id
        self.batch_size = batch_size
        self.memory = deque(maxlen=max_len_queue)
        self.dqnAlgo = DQN(batch_size=batch_size)
        self.action = None
        self.rewards = []
        
    def remember(self, state, action, reward, next_state):
        """
        The function takes in the current state, the action taken, the reward received, and the next state,
        and then adds them to the memory.
        
        :param state: the current state of the environment
        :param action: the action that the agent took in the current state
        :param reward: the reward that the agent gets after taking the action
        :param next_state: The next state of the environment
        """
        self.memory.append((state, action, reward, next_state))

    def get_action(self,state):
        """
        The function takes in a state and returns an action. 
        
        The action is determined by the DQN algorithm. 
        
        The DQN algorithm is a deep neural network that takes in a state and returns an action. 
        
        The DQN algorithm is trained by the fit function. 
        
        The fit function takes in a state and returns an action. 
        
        The fit function is a deep neural network that takes in a state and returns an action. 
        
        The fit function is trained by the fit function. 
        
        The fit function takes in a state and returns an action. 
        
        The fit function is a deep neural network that takes in a state and returns an action. 
        
        The fit function is trained by the fit function. 
        
        The fit function takes in a state and returns an action. 
        
        The fit function is a deep neural network that takes in a state and returns an action.
        
        :param state: the current state of the environment
        :return: The action that the agent will take.
        """
        self.action = self.dqnAlgo.fit(state)
        return self.action

    def replay_bufer(self,state,action,reward,next_state):
        """
        The function takes in the current state, the action taken, the reward received, and the next
        state. 
        
        It then adds the current state, action, reward, and next state to the memory. 
        
        If the memory is greater than the batch size, then the DQN algorithm is used to replay the
        memory. 
        
        The replay function is defined in the DQN algorithm class. 
        
        The replay function is defined in the DQN algorithm class. 
        
        The replay function is defined in the DQN algorithm class. 
        
        The replay function is defined in the DQN algorithm class. 
        
        The replay function is defined in the DQN algorithm class. 
        
        The replay function is defined in the DQN algorithm class. 
        
        The replay function is defined in the DQN algorithm class. 
        
        The replay function is defined in the DQN algorithm class.
        
        :param state: The current state of the environment
        :param action: The action that the agent took
        :param reward: The reward that the agent received for taking the action
        :param next_state: The next state after the action is performed
        """
        self.remember(state,action,reward, next_state)
        if len(self.memory) > self.batch_size:
            self.dqnAlgo.replay(self.memory)
    
    def plot_reward(self,with_agents,with_predicted_position,Random,without_restart, step=5 , color="blue"): # step=5
        """
        It plots the reward for each episode, and saves the plot as a png file
        
        :param number_of_senario: The number of the senario that we are running
        :param step: The number of episodes between each pair of (reward, episode), defaults to 5
        (optional)
        :param color: The color of the line, defaults to blue (optional)
        """
        plt.figure(figsize=(6, 4))
        plt.title(self.dqnAlgo.algorithm_name)
        plt.plot([i for i, x in enumerate(self.rewards) if i%step==0],
                 [x for i, x in enumerate(self.rewards) if i%step==0], color=color)
        plt.xlabel('Episodes')
        plt.ylabel('Total Reward per Epidode')
        n = len(self.rewards)
        plt.vlines(x=[i for i in range(n) if i%100==0], ymin=[min(self.rewards) for i in range(n) if i%100==0], ymax=[max(self.rewards) for i in range(n) if i%100==0], colors=['r' for i in range(n) if i%100==0], ls='--', lw=2)
        folder_name = ""
        if with_agents and with_predicted_position:folder_name = "Results_with_predicted_position"
        elif with_agents and not with_predicted_position:folder_name = "Results_without_predicted_position"
        elif not with_agents and not with_predicted_position:folder_name = "Results_without_agents"
        if Random : folder_name = "Results_Random"
        if without_restart:folder_name = "Results_without_restart"
        print(os.path.join(os.path.join(os.path.join(os.path.abspath("."),'resultes'),folder_name),"agent number "+str(self.agent_id)+".png"))
        plt.savefig(os.path.join(os.path.join(os.path.join(os.path.abspath("."),'resultes'),folder_name),"agent number "+str(self.agent_id)+".png"))
        # plt.show()