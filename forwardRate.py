import numpy as np

class ForwardRate:
    def __init__(self, r_1, r_2, t_1, t_2) -> None:
        self.r_1 = r_1
        self.r_2 = r_2
        self.t_1 = t_1
        self.t_2 = t_2
    
    def simple_forward_rate(self):
        return 1 /(self.t_2 - self.t_1) * ((1 + self.r_2 * self.t_2)/(1 + self.r_1 * self.t_1) - 1)
    
    def yearly_compounded_rate(self):
        return ((1 + self.r_2)**self.t_2 / (1 + self.r_1)**self.t_1)**(1/(self.t_2 - self.t_1)) - 1
    
    def continuously_compounded_rate(self):
        return (self.r_2 * self.t_2 - self.r_1 * self.t_1) / (self.t_2 - self.t_1)