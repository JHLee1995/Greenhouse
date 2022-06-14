from gym.spaces import Discrete
import random

class GreenHouse:
    """
        Initial
            * choose the 4 variables to determine the plant growth
                - temperature  -> cur_temp
                - humidity     -> cur_humidity
                - co2 level    -> cur_co2
                - light        -> cur_par

            * set and random outdoor environment and weather 
                - temperature  -> out_temp
                - humidity     -> out_humidity
                - co2 level    -> out_co2
                - light        -> out_par
    """
    def __init__(self):
        self.action_space = Discrete(8)

        self.cur_mass = 10 + random.randint(-2, 2)
        self.harvest_round = 300

        self.min_temp = 55
        self.max_temp = 80
        self.cur_temp = 45 + random.randint(-1, 1)

        self.min_humidity = 60
        self.max_humidity = 100
        self.cur_humidity = 50 + random.randint(-5, 5)

        self.min_co2 = 300
        self.max_co2 = 1500
        self.cur_co2 = 300 + random.randint(-250, 250)

        self.out_temp = random.randint(50, 90)
        self.out_humidity = random.randint(50, 95)
        self.out_co2 = random.randint(100, 2000)
        
        self.out_par = 0
    
        random_weather = Discrete(3)
        self.weather_set(random_weather.sample())

        self.cur_par = self.out_par

        self.ROOF_VENT_OPEN = True
        self.roof_duration = 5

        self.SHUTTER_OPEN = True
        self.shutter_duration = 5

        self.state = (
            self.cur_mass, 
            self.cur_temp, self.cur_humidity, self.cur_co2, 
            self.cur_par, self.out_par,
            self.out_temp, self.out_humidity, self.out_co2
        )

    """
        reset the current environment
    """

    def reset(self):
        self.cur_mass = 10 + random.randint(-2, 2)
        self.harvest_round = 300

        self.cur_temp = 45 + random.randint(-1, 1)
        self.cur_humidity = 50 + random.randint(-5, 5)
        self.cur_co2 = 300 + random.randint(-250, 250)
    
        self.out_temp = random.randint(50, 90)
        self.out_humidity = random.randint(50, 95)
        self.out_co2 = random.randint(100, 2000)
        self.out_par = 0

        random_weather = Discrete(3)
        self.weather_set(random_weather.sample())

        self.cur_par = self.out_par

        self.ROOF_VENT_OPEN = True
        self.roof_duration = 5

        self.SHUTTER_OPEN = True
        self.shutter_duration = 5

        self.state = (
             self.cur_mass, 
             self.cur_temp, self.cur_humidity, self.cur_co2, 
             self.cur_par, self.out_par,
             self.out_temp, self.out_humidity, self.out_co2
        )

        return self.state

    """
        Step
            * record the current weight bofore the impact of action to determine the reward
            * if variavle is out of boundary set reward equal to -1
            * if action's impact bring the weight increase set reward equal to 1 else -1
    """

    def step(self, action):
        prev_mass = self.cur_mass
        self.harvest_round -= 1

        self.environment_interaction(action)

        if not self.indoor_variable_boundary_valid():
            self.environment_for_growth()
        else:
            self.cur_mass -= 1
       
        if self.cur_mass - prev_mass > 0:
            reward = 1
        else:
            reward = -1

        if self.harvest_round == 0:
            done = True
        else:
            done = False

        state = (
             self.cur_mass, 
             self.cur_temp, self.cur_humidity, self.cur_co2, 
             self.cur_par, self.out_par, 
             self.out_temp, self.out_humidity, self.out_co2
        )

        return state, reward, done

    """
        Check the variable is valid or not
            * compare current with min/max boundary
    """
    def indoor_variable_boundary_valid(self):
        if self.cur_temp > self.max_temp or self.cur_temp < self.min_temp:
            return True
        elif self.cur_co2 > self.max_co2 or self.cur_co2 < self.min_co2:
            return True
        elif self.cur_humidity > self.max_humidity or self.cur_humidity < self.min_humidity:
            return True

        return False


    """
        Set random weather 
            * 0 : clear day
                with better lighting conditions, plant photosynthesis increasing
                    - temperature incresing
                    - humidity decreasing
                    - co2 decreasing

            * 1 : cloudy day
                with moderate lighting conditions, plant photosynthesis decreasing
                    - temperature increasing moderately 
                    - humidity increasing moderately
                    - co2 increasing

            * 2 : raniny day
                with worst lighting conditions, plant almost stop photosynthesis
                    - temperature decreasing
                    - humidity increasing sharply
                    - co2 increasing 
    """
    def weather_set(self, cur_weather):
        if cur_weather == 0:
            self.out_par += random.randint(500, 800)
            self.out_temp += random.randint(1, 10)
            self.out_humidity += random.randint(-10, 10)
            self.out_co2 += random.randint(-250, -200)
        elif cur_weather == 1:
            self.out_par += random.randint(200, 499)
            self.out_temp += random.randint(-5, 5)
            self.out_humidity += random.randint(1, 10)
            self.out_co2 += random.randint(1, 200)
        else:
            self.out_par += random.randint(1, 199)
            self.out_temp += random.randint(-10, -1)
            self.out_humidity += random.randint(15, 20)
            self.out_co2 += random.randint(150, 300)



    def environment_interaction(self, action):
        if action == 0:
            self.heater()
        elif action == 1:
            self.cooler()
        elif action == 2:
            self.humidity_controller()
        elif action == 3:
            self.co2_controller()
        elif action == 4:
            self.shutter()
        elif action == 5:
            self.roof_vent()
        elif action == 6:
            self.HAF_FANS()
        else:
            self.maintain()


    """
        Check the environment is good for plant growth
            * narrow the range which good for plant growth to make sure training steps are useful
            * avoid the situation like every possible action could make plant growth
            * when the shutter open, add photosynthesis help plant growth
    """
    def environment_for_growth(self):
        if (self.cur_temp > 62 and self.cur_temp < 68 
        and self.cur_humidity > 70 and self.cur_humidity < 75 
        and self.cur_co2 > 1000 and self.cur_co2 < 1200):
            self.cur_mass += 1

        if self.cur_par != 0:
            self.photosynthesis()

    def photosynthesis(self):
        round = 5
        while round:
            self.cur_co2 -= 10
            self.cur_humidity -= 1
            round -= 1

        self.cur_mass += 1        


    """
        Actions
            * narrow the impact of each action, make each action bring the unique variable change
            * 0 : heater     control
            * 1 : cooler     control
            * 2 : humidity   control
            * 3 : co2 level  control
            * 4 : shutter    control
            * 5 : roof vent  control
            * 6 : FANS       control
            * 7 : maintain do nothing
    """
    def heater(self):
        self.cur_temp += 1

    def cooler(self):
        self.cur_temp -= 1

    def humidity_controller(self):
        self.cur_humidity += 3

    def co2_controller(self):
        self.cur_co2 += 50

    def HAF_FANS(self):
        self.cur_temp -= 3
        self.cur_humidity -= 3

    def maintain(self):
        pass
    
    """
        Shutter & Roof Vent control
            * set initial round with 5
            * if round finished, set shutter/ roof vent close(False)
            * after the first round is finished, the subsequent action will set the round as 5 and open again
            * shutter open will directly get outdoor light
            * roof vent open will let the indoor environment interact with the outdoor environment
    """
    def shutter(self):
        if self.SHUTTER_OPEN and self.shutter_duration != 0:
            self.cur_par = self.out_par
            self.shutter_duration -= 1
        elif self.SHUTTER_OPEN and self.shutter_duration == 0:
            self.cur_par = 0
            self.SHUTTER_OPEN = False
        else:
            self.cur_par = self.out_par
            self.shutter_duration = 5
            self.SHUTTER_OPEN = True
            self.shutter_duration -= 1
             
    def roof_vent(self):
        if self.ROOF_VENT_OPEN and self.roof_duration != 0:
            self.interaction_with_outside()
            self.roof_duration -= 1
        elif self.ROOF_VENT_OPEN and self.roof_duration == 0:
            self.ROOF_VENT_OPEN = False
        else:
            self.interaction_with_outside()
            self.roof_duration = 5
            self.ROOF_VENT_OPEN = True
            self.roof_duration -= 1

    """ 
        Indoor environment interact with outdoor environment
            * set an factor let the indoor interact with outdoor slowly    
    """
    def interaction_with_outside(self):
        temp_offset = self.cur_temp - self.out_temp
        humidity_offset = self.cur_humidity - self.out_humidity
        co2_offset = self.cur_co2 - self.out_co2

        gradient = random.uniform(0.1, 0.5)
        
        self.cur_temp += gradient * (abs(temp_offset) if temp_offset < 0 else temp_offset)
        self.cur_humidity += gradient * (abs(humidity_offset) if humidity_offset < 0 else humidity_offset)
        self.cur_co2 += gradient * (abs(co2_offset) if co2_offset < 0 else co2_offset)

    

    

    



    







