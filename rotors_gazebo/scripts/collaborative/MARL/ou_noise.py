
import numpy as np
import numpy.random as nr

class OUNoise:
    """docstring for OUNoise"""
    def __init__(self,action_dimension,mu=0, theta=0.15, sigma=0.01):
        self.action_dimension = action_dimension
        self.mu = mu
        self.theta = theta
        self.sigma = sigma
        self.state = np.ones(self.action_dimension) * self.mu
        self.reset()

    def reset(self):
        self.state = np.ones(self.action_dimension) * self.mu

    def noise(self):
        x = self.state
        dx = self.theta * (self.mu - x) + self.sigma * nr.randn(x.shape[0],x.shape[1])
        self.state = x + dx
        return self.state

if __name__ == '__main__':
    ou = OUNoise(3)
    states = []
    for i in range(1000):
        states.append(ou.noise())
    import matplotlib.pyplot as plt

    plt.plot(states)
    plt.show()
