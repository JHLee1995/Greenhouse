"""
    Designed for GreenHouse Simulating

    * Basic variable control for plant growth
    1. Temperature
    2. Humidity
    3. CO2

    * Action take 
    1. Adjust temperatue controller
        - 50F < enviroment temperature < 80F ?

    2. Adjust humidifier
        - environment humidity < 70%

    3. CO2 tank       
        - environment co2 level 300 - 1500 ppm

    4. Roof vent  
        - indoor/outdoor temperature
        - co2 level decrease
        - indoor/outdoor humidity         
"""

import numpy as np
import random


class GreenHouse:
    ready_harvest = False
    curr_weight = 15
    harvest_weight = 95         # 95g is ready for harvest

    curr_temperature = 50       # fahrenheit degree
    min_temperature = 1
    max_temperature = 100

    curr_humidity = 70          # humidity percent
    min_humidity = 1            
    max_humidity = 100

    curr_co2 = 300              # co2 level
    min_co2 = 100
    max_co2 = 1500

    root_vent = False
    HAF_fans = False

    def __init__(self, curr_weight, curr_temperature, curr_humidity, curr_co2,
                harvest_weight, min_temperature, max_temperature, 
                min_humidity, max_humidity, min_co2, max_co2):

        self.curr_weight = curr_weight
        self.curr_temperature = curr_temperature
        self.curr_humidity = curr_humidity
        self.curr_co2 = curr_co2

        self.min_temperature = min_temperature
        self.max_temperature = max_temperature

        self.min_humidity = min_humidity
        self.max_humidity = max_humidity

        self.min_co2 = min_co2
        self.max_co2 = max_co2


    def ready_for_harvest(self):
        if (self.curr_weight > self.harvest_weight):
            ready_harvest = True

    
    def action_list(self, actions):
        curr_action = np.argmax(actions)
        if curr_action == 0:
            self.temperature_controller()
        if curr_action == 1:
            self.humidifier_controller()
        if curr_action == 2:
            self.co2_controller()
        if curr_action == 3:
            self.roof_vent_controller()
        if curr_action == 4:
            self.fans_controller()
        if curr_action == 5:
            self.ready_for_harvest()