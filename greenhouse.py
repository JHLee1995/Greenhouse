from gym.spaces import Discrete, Box
from gym.utils import seeding
import numpy as np

class GreenHouse:
    def __init__(self):
        """
            * Variable for plant growth
            1. temperature
            2. humidity
            3. co2
        """
        self.ready_for_harvest = 95
        self.action_space = Discrete(5)

        self.cur_weight = 10 
        self.min_weight = 10
        self.max_weight = 95
        
        self.cur_temperature = 55 
        self.min_temperatue = 35
        self.max_temperature = 80

        self.cur_humidity = 55 
        self.min_humidity = 40
        self.max_humidity = 100

        self.cur_co2_level = 450
        self.min_co2_level = 300
        self.max_co2_level = 1500

        '''
            * More details for environment  
        '''
        # self.outside_temperatue = random.randint(50, 90)
        # self.outside_humidity = random.randint(50, 95)
        # self.outside_co2_level = random.randint(100, 2000)
        
        self.low = np.array([self.min_weight, self.min_temperatue, self.min_humidity, self.min_co2_level], dtype=np.int32)
        self.high = np.array([self.max_weight, self.max_temperature, self.max_humidity, self.max_co2_level], dtype=np.int32)

        self.state = np.array([self.cur_weight, self.cur_temperature, self.cur_humidity, self.cur_co2_level])
        self.observation_space = Box(self.low, self.high, dtype=np.int32)
        

    def step(self, action):
        prev_weight = self.cur_weight
        
        '''
            take action and check the variable boundary
            if the variable over the max range use clip function set it as the max
        '''
        self.plant_growth(action)
        self.cur_temperature = np.clip(self.cur_temperature, self.min_temperatue, self.max_temperature)
        self.cur_humidity = np.clip(self.cur_humidity, self.min_humidity, self.max_humidity)
        self.cur_co2_level = np.clip(self.cur_co2_level, self.min_co2_level, self.max_co2_level)

        self.environment_for_growth()

        '''
            set prev_weight to record the plant weight before the action
            difference represents the accumulation of plant weight
        '''
        if self.cur_weight - prev_weight > 0:
            reward = 1
        else:
            reward = -1

        '''
            If the plant weight matched the harvest weight
            treat one episode as done
        '''
        if self.cur_weight >= self.ready_for_harvest:
            done = True
        else:
            done = False

        cur_state = np.array([self.cur_weight, self.cur_temperature, self.cur_humidity, self.cur_co2_level])
        return cur_state, reward, done


    def reset(self):
        '''
            * reset the variable
        '''
        self.cur_weight = 10
        self.cur_temperature = 55
        self.cur_humidity = 55
        self.cur_co2_level = 450

        self.state = np.array([self.cur_weight, self.cur_temperature, self.cur_humidity, self.cur_co2_level])
        
        return self.state


    '''
        * action take 
        0. adjust temperature 
            - 50F < enviroment temperature < 80F 

        1. adjust humidifier
            - 40 < environment humidity < 100

        2. co2 tank      
            - 300 < environment co2 level < 1500

        3. roof vent  
            - indoor/outdoor temperature
            - co2 level decrease
            - indoor/outdoor humidity    

        5. fans
            - indoor temperature
            - indoor humidity

        6. maintain the current environment
            - indoor temperature/humidity/co2
    '''
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
        elif action == 5:
            self.maintain_current_environment()

        
    '''
        Check if the environment good for growth
        expanded the range for growth to accelerate training speed
    '''
    def environment_for_growth(self):
        if (self.cur_temperature > 40 and self.cur_temperature < 75 
        and self.cur_humidity > 45 and self.cur_humidity < 95 
        and self.cur_co2_level > 500 and self.cur_co2_level < 1400):
            self.cur_weight += 5

    # Action 0
    def temperature_controller(self):
        self.cur_temperature += 3
        self.cur_humidity += 1

    # Action 1
    def humidifier_controller(self):
        self.cur_temperature += 1
        self.cur_humidity += 3

    # Action 2
    def co2_controller(self):
        self.cur_temperature -= 2
        self.cur_co2_level += 50

    # Action 3
    def roof_vent_controller(self):
        self.cur_temperature -= 5
        self.cur_humidity -= 3
        self.cur_co2_level -= 50

    # Action 4
    def fans_controller(self):
        self.cur_temperature -= 2
        self.cur_humidity -= 2

    # Action 5
    def maintain_current_environment(self):
        pass

    
