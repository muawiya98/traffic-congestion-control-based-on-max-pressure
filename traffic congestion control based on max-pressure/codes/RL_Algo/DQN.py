
from codes.RL_Algo.RLAlgorithm import RLAlgorithm
from keras.layers import Dense, Input ,LeakyReLU
from keras.models import load_model as ldm
from keras.models import save_model as sdm
from keras.layers import Dense, Input
from keras.models import Sequential
from keras.optimizers import Adam
import numpy as np
import random
import os


class DQN(RLAlgorithm):
    # , env
    def __init__(self, epochs=100, max_steps=99,neurons_num:list = [128,32], lr=0.001, gamma=0.8, epsilon=0.5, decay=0.999, min_epsilon=0.1, batch_size=16):
        super().__init__(epochs, lr, gamma, epsilon, decay, min_epsilon)
        self.algorithm_name = "DQN"
        self.batch_size = batch_size
        self.neurons_num_list = neurons_num
        self.model = self.create_model()
        self.rewards = []
        # self.model.summary()
        

    def create_model(self):
        model = Sequential()
        model.add(Input(shape = 52))
        for n in self.neurons_num_list:
            model.add(Dense(n, activation=LeakyReLU(alpha=0.01)))
        model.add(Dense(1,activation='linear', name="Actions"))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.lr,decay=self.decay))
        return model

    def replay(self,memory):
        x_batch,y_batch=[],[]
        mini_batch = random.sample(memory, min(len(memory), self.batch_size))
        for state, action, reward, next_state in mini_batch:
            y_target = self.pred(state)
            y_target[0][0] = reward + self.gamma * self.Q_next(next_state)[0]
            x_batch.append(state)
            y_batch.append(y_target[0])
        self.model.fit(np.array(x_batch),np.array(y_batch),batch_size=len(x_batch), verbose=0)
        self.epsilon = max(self.epsilon * self.decay, self.min_epsilon)

    def Q_next(self, state):
        return self.pred(state)[0]

    def fit(self,state):
        return self.policy(state)

    def policy(self, state):
        rand = np.random.uniform(0, 1)
        if rand > self.epsilon:return self.value_function(state)
        else:
            temp = np.random.choice([0, 1])
            return [temp,1-temp]

    def pred(self, state):
        return self.model.predict(state, verbose=0)

    def value_function(self, state):
        result = self.pred(state)[0]
        result[0] = 1 if result[0] > 0 else 0
        return [result[0],1-result[0]]

    def save(self, path=".",file_name=None, *args):
        if os.path.isdir(path):
            if not path.endswith("rl_models"):
                models_path = os.path.join(path, "rl_models")
                if not os.path.isdir(models_path):os.mkdir(models_path)
            else:models_path = path
            if file_name:self.model.save_weights(os.path.join(models_path,file_name),*args)
            else:self.model.save_weights(os.path.join(models_path,"DQN"),*args)
        self.model.save_weights(path,*args)
    
    
    def save_model(self,path=".", file_name=None, *args):
        if os.path.isdir(path):
            if not path.endswith("rl_models"):
                models_path = os.path.join(path,"rl_models")
                if not os.path.isdir(models_path):os.mkdir(models_path)
            else:models_path = path
            if file_name:sdm(self.model, os.path.join(models_path,file_name),*args)
            else:sdm(self.model, os.path.join(models_path,"DQN.h5"),*args)
        sdm(self.model, path, *args)
    
    def load(self, path, *args):
        self.model.load_weights(path,*args)
    
    def load_model(self, path, *args):
        self.model = ldm(path, *args)