from abc import abstractmethod, ABC
import matplotlib.pyplot as plt

class RLAlgorithm(ABC):
    def __init__(self, total_episodes=10000, lr=0.5, gamma=0.9, epsilon=0.9, decay=0.99, min_epsilon=0.1):
        self.total_episodes = total_episodes
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.decay = decay
        self.min_epsilon = min_epsilon
        self.algorithm_name = ""
        self.rewards = []

    @abstractmethod
    def fit(self, *args, **kwargs):
        pass

    @abstractmethod
    def policy(self, *args, **kwargs):
        pass

    @abstractmethod
    def value_function(self, state: int, *args, **kwargs):
        pass

    @abstractmethod
    def save(self, path=".", file_name=None):
        pass

    @abstractmethod
    def load(self, path):
        pass

    def plot_reward(self, step=5 , color="blue"): # step=5
        step=int(len(self.rewards)/2)
        plt.figure(figsize=(6, 4))
        plt.title(self.algorithm_name)
        # Plot The Pair Of (Reward, Episodes) Each Step
        plt.plot([i for i, x in enumerate(self.rewards) if i % step == 0],
                 [x for i, x in enumerate(self.rewards) if i % step == 0], color=color)
        plt.xlabel('Episodes')
        plt.ylabel('Total Reward per Epidode')
        plt.show()
