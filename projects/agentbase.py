from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
import pandas as pd

class OccupantAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        # Implement the occupant's movement behavior here
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    
    def update_status(self, environmental_data):
        if 'occupant' in environmental_data:
            self.airQuality = environmental_data['occupant']

class ieq_priority(Agent):
        
    def check_ieq_priority_condition(thermal_satisfaction,visual_satisfaction,acoustical_satisfaction,air_quality_satisfaction,ieq_priority):

        if ((thermal_satisfaction == "Thermally_Hot" or thermal_satisfaction == "Thermally_Cold") and ieq_priority == "Thermal_Comfort"):
            ieq_priority_condition = True

        elif ((visual_satisfaction == "Bright_Light_With_View" or visual_satisfaction == "Dim_Light_With_View"or visual_satisfaction == "Dim_Light_With_No_View")and ieq_priority == "Visual_Comfort"):
            ieq_priority_condition = True

        elif (acoustical_satisfaction == "Acoustically_Dissatisfied" and ieq_priority == "Acoustical_Comfort"):
            ieq_priority_condition = True

        elif (air_quality_satisfaction == "Air_Quality_Dissatisfied" and ieq_priority == "AirQuality_Comfort"):
            ieq_priority_condition = True
        else :
            ieq_priority = False
        return ieq_priority_condition

    def check_ieq_priority_achieved_condition(thermal_satisfaction,visual_satisfaction,acoustical_satisfaction,air_quality_satisfaction,ieq_priority):

        if (
            thermal_satisfaction == "Thermally_Satisfied"
            and ieq_priority == "Thermal_Comfort"
        ):
            ieq_priority_achieved_condition = True

        elif (
            visual_satisfaction == "Sufficient_Light_With_View"
            and ieq_priority == "Visual_Comfort"
        ):
            ieq_priority_achieved_condition = True

        elif (
            acoustical_satisfaction == "Acoustically_Satisfied"
            and ieq_priority == "Acoustical_Comfort"
        ):
            ieq_priority_achieved_condition = True

        elif (
            air_quality_satisfaction == "Air_Quality_Satisfied"
            and ieq_priority == "AirQuality_Comfort"
        ):
            ieq_priority_achieved_condition = True
        
        else :
            ieq_priority_achieved_condition = False

        return ieq_priority_achieved_condition

    def check_ieq_second_choice_condition(
        thermal_satisfaction,
        visual_satisfaction,
        acoustical_satisfaction,
        ieq_second_choice,
    ):

        if (
            (thermal_satisfaction == "Thermally_Hot" or thermal_satisfaction == "Thermally_Cold")
            and ieq_second_choice == "Thermal_Comfort"
        ):
            ieq_second_choice_condition = True

        elif (
            (visual_satisfaction == "Bright_Light_With_View"
            or visual_satisfaction == "Dim_Light_With_View"
            or visual_satisfaction == "Dim_Light_With_No_View")
            and ieq_second_choice == "Visual_Comfort"
        ):
            ieq_second_choice_condition = True

        elif (
            acoustical_satisfaction == "Acoustically_Dissatisfied"
            and ieq_second_choice == "Acoustical_Comfort"
        ):
            ieq_second_choice_condition = True
        
        else:
            ieq_second_choice_condition = False

        return ieq_second_choice_condition

class LightAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        #self.is_on = False
        self.light = 0
        self.preferred_light = 44

    #def turn_on(self):
     #   self.is_on = True
      #  self.light = self.preferred_light

    #def turn_off(self):
     #   self.is_on = False
      #  self.light = 0
    
    
    def update_status(self, environmental_data):
            if 'Light' in environmental_data:
                self.light = int(environmental_data['Light'])
            #self.adjust_light()
            print(f"Preferred light: {self.preferred_light}")
            print(f"New light: {self.light}")
    def Light_satisfaction(self):
        if self.Light <= self.preferredLight:
            self.Light = 'Light_Satisfied'
        else:
            self.LightSatisfaction = 'Light_Dissatisfied'
        return self.LightSatisfaction

    def adjust_light(self):
        #print(f"Current light: {self.light}, Preferred light: {self.preferred_light}")
        while self.light != self.preferred_light:
            if self.light < self.preferred_light:
                self.light += 1  # Increment light
                print("Incrementing light by 1")
            elif self.light > self.preferred_light:
                self.light -= 1  # Decrement light
                print("Decrementing light by 1")
        print(f"Current light: {self.light}, Preferred light: {self.preferred_light}")

    #def set_preferred_light(self, light):
     #   self.preferred_light = light 

class TemperatureController(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
        self.preferredTemperature = 22  # Default preferred temperature
        self.Temperature = 0

    
    def update_state(self, environmental_data):
        if 'Temperature' in environmental_data:
            self.Temperature = environmental_data['Temperature']
            print(f"New Temperature: {self.Temperature}")
            print(f"Preferred Temperature: {self.preferredTemperature}")
    def temperature_satisfaction(self):
        if self.Temperature <= self.preferredTemperature:
            self.Temperature = 'Temperature_Satisfied'
        else:
            self.TemperatureSatisfaction = 'Temperature_Dissatisfied'
        return self.TemperatureSatisfaction
    
    def adjust_temperatue(self):
        #print(f"Current Temperature: {self.Temperature}, Preferred Temperature: {self.preferredTemperature}")
        while self.Temperature != self.preferredTemperature :
            if self.Temperature < self.preferredTemperature:
                self.Temperature += 1  # Increment temperature by 1
                print("Incrementing temperature by 1")
            elif self.Temperature > self.preferredTemperature:
                self.Temperature -= 1  # Decrement temperature by 1
                print("Decrementing temperature by 1")
            # Update the temperature to the preferred temperature
        print(f"Current Temperature: {self.Temperature}, Preferred Temperature: {self.preferredTemperature}")
        
    #def set_preferred_temperature(self, temperature):
     #   self.preferredTemperature = temperature 

class AirQualityManager(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.preferredAirQuality = 33  # Set the preferred air quality
        self.airQuality = 0

    def update_state(self, environmental_data):
        if 'Air Quality' in environmental_data:
            self.airQuality = int(environmental_data['Air Quality'])
        #self.air_quality_satisfaction()
        #self.adjust_air_quality()  # Adjust the environment based on the assessment
        print(f"New air quality: {self.preferredAirQuality}")
        print(f"Preferred air quality: {self.airQuality}")

    def air_quality_satisfaction(self):
        if self.airQuality <= self.preferredAirQuality:
            self.airQualitySatisfaction = 'Air_Quality_Satisfied'
        else:
            self.airQualitySatisfaction = 'Air_Quality_Dissatisfied'
        return self.airQualitySatisfaction

    def adjust_air_quality(self):
        # Incrementally adjust the air quality towards the preferred air quality
        while self.airQuality != self.preferredAirQuality:
            if self.airQuality > self.preferredAirQuality:
                self.windowStatus = 'Opened'
                self.airQuality -= 1  # Example decrement
                print("Decrementing air quality by 1")
            elif self.airQuality < self.preferredAirQuality:
                self.windowStatus = 'Closed'
                self.airQuality += 1  # Example increment
                print("Incrementing air quality by 1")
        print(f"Current air quality: {self.airQuality}, Preferred air quality: {self.preferredAirQuality}")
    
    #def set_preferred_air_quality(self, air_quality):
     #   self.preferredAirQuality = air_quality

class AcousticsManager(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.preferredAcoustics = 4  # Set the preferred acoustics level
        self.acoustics = 0

    
    def update_state(self, environmental_data):
        if 'Acoustics' in environmental_data:
            self.acoustics = int(environmental_data['Acoustics'])
        #self.acoustical_satisfaction()
        #self.adjust_acoustics()  # Adjust the acoustics based on the assessment
        print(f"New acousitics: {self.acoustics}")
        print(f"Preferred acousitics: {self.preferredAcoustics}")

    def acoustical_satisfaction(self):
        if self.acoustics <= self.preferredAcoustics:
            self.acousticalSatisfaction = 'Acoustically_Satisfied'
        elif self.acoustics > self.preferredAcoustics:
            self.acousticalSatisfaction = 'Acoustically_Dissatisfied'
        else:
            self.acousticalSatisfaction = 'Neutral'
        return self.acousticalSatisfaction

    def adjust_acoustics(self):
        # Incrementally adjust the acoustics towards the preferred acoustics level
        while self.acoustics != self.preferredAcoustics:
            if self.acoustics > self.preferredAcoustics:
                # Simulate actions that improve acoustics
                self.windowStatus = 'Closed'
                self.acoustics -= 1  # Example decrement
                print("Decrementing acoustics by 1")
            elif self.acoustics < self.preferredAcoustics:
                # Simulate actions that worsen acoustics
                self.windowStatus = 'Opened'
                self.acoustics += 1  # Example increment
                print("Incrementing acoustics by 1")
        print(f"Current Acoustics: {self.acoustics}, Preferred Acoustics: {self.preferredAcoustics}")
    #def set_preferred_acoustics(self, acoustics):
     #   self.preferredAcoustics = acoustics

class WindowAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.window_status = None  # Window is initially closed
        self.windowAttitude = 3
        self.windowPercievedNorm =3
        self.windowPercievedBehavioralControl = 4

    def calculate_window_intention(self, windowAttitude, windowPercievedNorm, windowPercievedBehavioralControl):
        window_Intention=(windowAttitude + windowPercievedNorm + windowPercievedBehavioralControl) / 3
        return window_Intention

    #def check_window_status(self,windowIntention, windowStatus):
     #if windowIntention >= 4 and windowStatus == "Closed":
      #  self.windowStatus = "Opened"
    # elif windowIntention < 4 and windowStatus == "Closed":
     #   self.windowStatus = "Closed"

     #return windowStatus
        
    def adjust_window_status(self, windowAttitude, windowPercievedNorm, windowPercievedBehavioralControl, thermalSatisfaction, visualSatisfaction, IEQPriority, beliefTowardsOperatingWindow_Temperature):
        windowIntention = self.calculate_window_intention(windowAttitude, windowPercievedNorm, windowPercievedBehavioralControl)

        if (windowIntention >= 4 and self.windowStatus == 'Closed' and thermalSatisfaction == 'Thermally_Cold' and visualSatisfaction == 'Dim_Light_With_View' and IEQPriority == 'Thermal_Comfort' and beliefTowardsOperatingWindow_Temperature == 'Improve_Temperature'):
            self.windowStatus = 'Opened'

        elif (windowIntention >= 4 and thermalSatisfaction == "Thermally_Hot" and
        IEQPriority == "Thermal_Comfort" and
        self.windowStatus == "Closed" and
        beliefTowardsOperatingWindow_Temperature == "Improve_Temperature"):
            self.window_status = "Opened"

        elif (thermalSatisfaction == "Thermally_Cold" and
        IEQPriority == "Thermal_Comfort" and
        self.windowStatus == "Closed" and
        beliefTowardsOperatingWindow_Temperature == "Improve_Temperature" and
        windowIntention >= 4):
            self.window_status = "Opened"
        elif (thermalSatisfaction == "Thermally_Cold" and
        IEQPriority == "Thermal_Comfort" and
        self.windowStatus == "Opened" and
        beliefTowardsOperatingWindow_Temperature == "Improve_Temperature" and
        windowIntention >= 4):
            self.window_status = "Closed"
        elif windowIntention < 4 and self.windowStatus == 'Closed':
            self.windowStatus = 'Closed'
        return self.windowStatus

    #def step(self, main):
        # Use main model attributes to recalculate window intention
        windowIntention = self.recalculate_window_intention_based_on_conditions(main)
        self.adjust_window_status(windowIntention)
        # Additional logic can be added here

    def update_state(self, environmental_data):
        if 'window_status' in environmental_data:
            self.window_status = environmental_data['window_status']
        self.calculate_window_intention(self)
        self.adjust_window_status(self)
        # Update logic for WindowAgent based on environmental data
        # Replace with actual update logic

class BlindAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.blindStatus = None
        self.blindAttitude =3 
        self.blindPercievedNorm =3 
        self.blindPercievedBehavioralControl =3

    def calculate_blind_intention(self,blindAttitude, blindPercievedNorm, blindPercievedBehavioralControl):
        blind_intention = (blindAttitude + blindPercievedNorm + blindPercievedBehavioralControl) / 3
        return blind_intention
    
    def adjust_blind_status(self, blindIntention, visualSatisfaction):
        if blindIntention >= 4:
            if self.blindStatus == 'closed' and visualSatisfaction == 'Dim_Light_With_No_View':
                self.blindStatus = 'opened'
            elif self.blindStatus == 'opened' and visualSatisfaction == 'Bright_Light_With_View':
                self.blindStatus = 'tilted'
            elif self.blindStatus == 'tilted' and visualSatisfaction == 'Bright_Light_With_View':
                self.blindStatus = 'closed'
        else:
            if self.blindStatus == 'closed':
                self.blindStatus = 'closed'
            elif self.blindStatus == 'opened':
                self.blindStatus = 'opened'
            # Note: You may want to handle the 'tilted' case explicitly here if needed

        return self.blindStatus
    
    def update_state(self, environmental_data):
        if 'blindstatus' in environmental_data:
            self.blindStatus = environmental_data['window_status']
        self.calculate_blind_intention(self)
        self.adjust_blind_status(self)
        # Update logic for WindowAgent based on environmental data
        # Replace with actual update logic

class ViewMonitor(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.view = None

    def assess_view(self, blindStatus):
        if blindStatus == 'closed':
            self.view = 'No_View'
        else :
            self.view = 'View'
        return self.view

class VisualEnvironmentManager(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.visualSatisfaction = None

    def assess_visual_satisfaction(self, blindStatus, light, rectangle):
        if blindStatus == 'closed' and light <= 50:
            self.visualSatisfaction = 'Dim_Light_With_No_View'
            rectangle.setFillColor('black')
        elif blindStatus in ['opened', 'tilted'] and light <= 50:
            self.visualSatisfaction = 'Dim_Light_With_View'
            rectangle.setFillColor('black')
        elif blindStatus == 'tilted' and 50 <= light <= 100:
            self.visualSatisfaction = 'Sufficient_Light_With_View'
            rectangle.setFillColor('yellow')
        elif blindStatus == 'opened' and 50 <= light <= 100:
            self.visualSatisfaction = 'Sufficient_Light_With_View'
            rectangle.setFillColor('yellow')

        return self.visualSatisfaction

class RoomModel(Model):
    def __init__(self, width, height, day_night_cycle):
        self.num_agents =  7 # One for occupant, one for light
        self.grid = SingleGrid(width, height, True)
        self.day_night_cycle = day_night_cycle
        self.current_step = 0
        self.schedule = RandomActivation(self)
        self.environment_data = pd.read_csv(r'/Users/shaikmohammadshaid/Desktop/projects/new_dataset.csv')
        self.environment_data_index = 0  # To keep track of the current row


        # Create the occupant agent
        agent = OccupantAgent(0, self)
        x, y = 2, 3  # Replace with your desired coordinates
        self.grid.place_agent(agent, (x, y))
        self.schedule.add(agent)
        self.occupant = agent  # Store reference to the occupant


        # Create the air conditioner agent
        temperature = TemperatureController(4, self)
        self.temperature_position = (1, 5)  # Position where the air conditioner is placed
        self.grid.place_agent(temperature, self.temperature_position)
        self.schedule.add(temperature)
        self.temperature = temperature  # Store reference to the air conditioner

        air_quality = AirQualityManager(1,self)
        self.air_quality_position = (3,5)
        self.grid.place_agent(air_quality,self.air_quality_position)
        self.schedule.add(air_quality)
        self.air_quality = air_quality

        acoustic = AcousticsManager(2, self)
        self.acoustic_position = (5, 5)  # Position where the window control manager is placed
        self.grid.place_agent(acoustic, self.acoustic_position)
        self.schedule.add(acoustic)
        self.acoustic = acoustic  # Store reference to the window control manager

        light = LightAgent(3, self)  # Updated unique ID for LightAgent
        self.light_position = (7, 5)  # Choose appropriate position
        self.grid.place_agent(light, self.light_position)
        self.schedule.add(light)
        self.light = light  # Store reference to the light agent



    def get_environmental_data(self):
        # Check if the index is still within the range of the DataFrame
        if self.environment_data_index < len(self.environment_data):
            row = self.environment_data.iloc[self.environment_data_index]
            print("Fetching row at index", self.environment_data_index, ":", row)  # Print the fetched row
            self.environment_data_index += 1  # Move to the next row for the next step
            return row.to_dict()
            print("Environmental data:", self.get_environmental_data())  # Diagnostic print
            return self.environment_dict
        else :
            return None

    def get_data(self):
        # Logic to extract and return data from the model
        data = {
            "temperature": self.temperature.Temperature,
            "light" : self.light.Light,
            "airQuality" : self.air_quality.airQuality, # Example data
            "Acoustics" : self.acoustic.acoustics,
            # Add more data points as needed
        }
        return data

    def step(self):
        print("Step function called, Current Step:", self.current_step)
        environmental_data = self.get_environmental_data()

        if environmental_data:
            # Update the preferred state of each agent based on environmental data
            for agent in self.schedule.agents:
                if hasattr(agent, 'update_state'):
                    agent.update_state(environmental_data)
            
            all_agents_at_preferred_state = False

            while not all_agents_at_preferred_state:
                all_agents_at_preferred_state = True

                # Check and adjust for each agent
                for agent in self.schedule.agents:
                    if isinstance(agent, LightAgent):
                        agent.adjust_light()
                        #print(f"LightAgent: Current light {agent.light}, Preferred light {agent.preferred_light}")
                        if agent.light != agent.preferred_light:
                            all_agents_at_preferred_state = False

                    elif isinstance(agent, TemperatureController):
                        agent.adjust_temperatue()
                        #print(f"Adjusting temperature: Current temperature {agent.Temperature}, Preferred temperature {agent.preferredTemperature}")
                        if agent.Temperature != agent.preferredTemperature:
                            all_agents_at_preferred_state = False
                    
                    elif isinstance(agent, AirQualityManager):
                        agent.adjust_air_quality()
                        #print(f"Adjusting air quality: Current air quality {agent.airQuality}, Preferred air quality {agent.preferredAirQuality}")
                        if agent.airQuality != agent.preferredAirQuality:
                            all_agents_at_preferred_state = False


                    elif isinstance(agent, AcousticsManager):
                            agent.adjust_acoustics()
                            #print(f"Adjusting acoustics: Current acoustics {agent.acoustics}, Preferred acoustics {agent.preferredAcoustics}")
                            if agent.acoustics != agent.preferredAcoustics:
                                all_agents_at_preferred_state = False
                    # Similar blocks for TemperatureController, AirQualityManager, AcousticsManager
                    

                    self.schedule.step()
                    self.current_step += 1
                    #print("Proceeding to next step...")

            # Update the state of each agent based on the adjusted environmental conditions
            for agent in self.schedule.agents:
                if hasattr(agent, 'update_status'):
                    agent.update_status(environmental_data)

            # Proceed with the next step
            if all_agents_at_preferred_state:
                self.schedule.step()
                self.current_step = int(environmental_data['Time'])
                #print("Proceeding to next step...")
             
def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5, "Layer": 0}
    if isinstance(agent, OccupantAgent):
        portrayal["Color"] = "blue"

    elif isinstance(agent, AirQualityManager):
        portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5, "Layer": 0}
        if agent.airQuality >= agent.preferredAirQuality:
            portrayal["Color"] = "green"  
        #elif 380 < agent.airQuality > agent.preferredAirQuality:
         #   portrayal["Color"] = "blue"   
        else:
            portrayal["Color"] = "gray" 
    elif isinstance(agent, AcousticsManager):
        portrayal = {"Shape": "rect", "Filled": "true", "w": 0.5,"h": 0.5, "Layer": 0}
        if agent.acoustics >= agent.preferredAcoustics:
            portrayal["Color"] = "green"  
        else :
            portrayal["Color"] = "gray" 
    elif isinstance(agent, LightAgent):
        # Corrected attribute name to 'light'
        if agent.light >= agent.preferred_light:  
            portrayal["Color"] = "green"
        #elif 60 <= agent.light < agent.preferred_light:
         #   portrayal["Color"] = "orange"  
        else:
            portrayal["Color"] = "gray" 

    elif isinstance(agent, TemperatureController):
        if agent.Temperature >= agent.preferredTemperature:
             portrayal["Color"] = "green"  
        elif agent.Temperature < agent.preferredTemperature:
            portrayal["Color"] = "gray"
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
day_night_cycle = [True, False, True, False]  # Extend this based on your simulation needs
server = ModularServer(RoomModel, [grid], "Room Model", {"width": 12, "height": 12 ,"day_night_cycle": day_night_cycle })
server.launch(port=5001)  # Specify the port as an argument here 
#server.stop(port=5507)
