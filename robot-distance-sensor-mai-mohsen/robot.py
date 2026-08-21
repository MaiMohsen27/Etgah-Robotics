"""
Robot Distance Sensor Program
------------------------------
Problem Discription: 

This program models a robot with a front distance sensor.
The sensor produces a list of distance readings (in meters), and for
each reading the robot must decide what action to take:
 
    - distance < 0.5m        -> STOP      (obstacle too close)
    - 0.5m <= distance <= 1m -> SLOW      (obstacle nearby)
    - distance > 1m          -> MOVE FAST (path is clear)
 
What the program does: 

The Robot class stores basic robot info (name, battery level) and
provides a method to process a whole list of sensor readings at once,
returning the correct action for each one. Invalid readings (non-numeric
or negative values) are handled with error messages.
"""
class Robot:
    def __init__(self, name, battery):
        #Initializes the Robot instance with a name and initial battery level.
        self.name = name
        self.battery = battery
        
    def action(self, distances):
        """
        Processes a list of distance sensor measurements (in meters) 
        and determines the robot action for each.
        
        Raises an error if the distance is not a valid number
        or if it is negative (since a negative distance makes no
        physical sense).
        """
        print(f"\n--- Robot '{self.name}' (Battery: {self.battery}%) Processing Distances ---")
        for index, distance in enumerate(distances, start=1):
            try:  
                #making sure the value is float
                distance = float(distance)
                
                #rejecting negative readings
                if distance < 0:
                    print(f"\nReading #{index} ({distance}): Error -> Distance cannot be negative.")      
                elif distance < 0.5:
                    print(f"\nReading #{index} ({distance} m): STOP (obstacle too close)") 
                elif distance <= 1:
                    print(f"\nReading #{index} ({distance} m): SLOW (obstacle nearby)") 
                else:
                    print(f"\nReading #{index} ({distance} m): MOVE FAST (path is clear)")
                
            #rejecting invalid data values and data types
            except (ValueError, TypeError):
                print(f"\nReading #{index} ({distance}): Error -> Invalid distance value. Must be a number.") 


# ---------------------------------------------------------------------
# TEST CODE
# ---------------------------------------------------------------------

if __name__ == "__main__":

    my_robot= Robot("May", 90)

    print("Test Case 1: Standard Valid Readings")
    tc1 = [0.2, 0.75, 1.5, 0.5, 1.0]
    my_robot.action(tc1)

    print("\n---------------------------------------")

    print("\nTest Case 2: Numeric Values as Strings")
    tc2 = ["0.3", "0.8", "2.5"]
    my_robot.action(tc2)

    print("\n---------------------------------------")

    print("\nTest Case 3: Error Handling for Non-Numeric Values")
    tc3 = [0.4, "invalid_val", None, 1.2]
    my_robot.action(tc3)

    print("\n---------------------------------------")

    print("\nTest Case 4: Error Handling for Negative Distances")
    tc4 = [-0.5, 0.8, -10.0, 1.1]
    my_robot.action(tc4)

    print("\n---------------------------------------")
    
    print("\nTest Case 5: boundary values (exactly 0.5 and 1)")
    tc5= [0.5, 1]
    my_robot.action(tc5)
  
