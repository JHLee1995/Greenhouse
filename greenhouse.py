"""
    Designed for GreenHouse Simulating

    * Basic variable control for plant growth
    1. Temperature
    2. Humidity
    3. CO2

    * Action take 
    1. Adjust temperatue controller
        - 50F < enviroment temperature < 80F 

    2. Adjust humidifier
        - environment humidity < 70%

    3. CO2 tank       
        - environment co2 level 300 - 1500 ppm

    4. Roof vent  
        - indoor/outdoor temperature
        - co2 level decrease
        - indoor/outdoor humidity         
"""

from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random

from numpy.random.mtrand import rand

class GreenHouse:
    def __init__(self):
        """
            Actions:
                0 : Temperature 
                1 : Humudity
                2 : CO2
                3 : Roof Vent
                4 : HAF Fans
        """
        self.action_space = Discrete(5)
        self.observation_space = Box(low = np.array([0]), high = np.array([100]))
        self.state = 10 + random.randint(0, 5)
        self.growth_duration = 90
        self.good_for_harvest = 95

        self.cur_temperature = 55 + random.randint(-1, 1)
        self.cur_humidity = 90 + random.randint(-3, 3)
        self.co2_level = 750 + random.randint(-50, 50)

    def step(self, action):
        prev_state = self.state
        self.state = self.plant_growth(action)
        self.growth_duration -= 1
        
        # Check reward by plant_growth function
        if self.state - prev_state > 0:
            reward = 1
        else:
            reward = -1

        # Check if growth is done
        if self.growth_duration <= 0:
            done = True
        else:
            done = False

        return self.state, reward, done


    def reset(self):
        self.state = 10 + random.randint(0, 5)
        self.growth_duration = 90

        self.cur_temperature = 55 + random.randint(-1, 1)
        self.cur_humidity = 90 + random.randint(-3, 3)
        self.cur_co2_level = 750 + random.randint(-50, 50)

        return self.state


    def plant_growth(self, action):
        if action == 0:
            self.temperature_controller()
        elif action == 1:
            self.humidifier_controller()
        elif action == 2:
            self.co2_controller()
        elif action == 3:
            self.roof_vent_controller()
        elif action == 4:
            self.fans_controller()

        self.environment_for_growth()

        return self.state
    
    def environment_for_growth(self):
        if self.cur_temperature > 50 and self.cur_temperature < 70:
            self.state += random.randint(1, 2)
        if self.cur_humidity > 65 and self.cur_humidity < 85:
            self.state += random.randint(1, 2)
        if self.cur_co2_level > 750 and self.cur_co2_level < 1150:
            self.state += random.randint(1, 3)


    # Action 0
    def temperature_controller(self):
        self.cur_temperature *= 1.5
        self.cur_humidity *= 1.5

    # Action 1
    def humidifier_controller(self):
        self.cur_temperature *= 1.2
        self.cur_humidity *= 1.5

    # Action 2
    def co2_controller(self):
        self.cur_temperature *= 0.9
        self.co2_level *= 1.5

    # Action 3
    def roof_vent_controller(self):
        self.cur_temperature *= 0.7
        self.cur_humidity *= 0.7
        self.cur_co2_level *= 0.6

    # Action 4
    def fans_controller(self):
        self.cur_temperature *= 0.9
        self.cur_humidity *= 0.9
    
        
  

    
