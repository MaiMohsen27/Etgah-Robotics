# Robot Distance Sensor Program

## 1. What does this program do?

This program simulates a robot that has a distance sensor on its front. 
The sensor takes multiple measurements and returns a list of distances (in meters). 
The program reads that list and, for each distance, decides what the robot should do:

- **Distance less than 0.5m** → `STOP` (obstacle too close)
- **Distance 0.5m to 1m** → `SLOW` (obstacle nearby)
- **Distance more than 1m** → `MOVE FAST` (path is clear)

It also handles bad sensor data: 
if a reading is negative or isn't a valid number, the program prints an error message.

## 2. How does the Robot class work?

The `Robot` class represents a single robot and stores two pieces of information about it:

- `name` : the robot's name
- `battery` : its current battery percentage

These are set once when a `Robot` object is created, using the `__init__` method:

```python
my_robot = Robot("May", 90)
```

The robot can be handed a list of distance readings using its `action()` method, which processes them one by one.

## 3. What does each method do?

- **`__init__(self, name, battery)`**
  Sets up a new robot with a given name and battery level. This runs automatically whenever a `Robot` object is created.

- **`action(self, distances)`**
  Takes a list of distance readings and loops through each one, in order:
  - Converts the value to a `float` so both numbers and numeric strings (like `"0.8"`) work.
  - If the value can't be converted to a number (e.g. `"invalid_val"` or `None`), it catches the error and prints an "Invalid distance value" message for that reading.
  - If the number is negative, it prints an error saying distance can't be negative.
  - Otherwise, it compares the distance against the thresholds and prints the correct action: `STOP`, `SLOW`, or `MOVE FAST`.
  - Every reading is checked independently, so one bad value in the list doesn't stop the rest from being processed.

## 4. How do I run the code?

1. Make sure Python 3 is installed on your computer.
2. Save the file (`robot.py`).
3. Open a terminal in the same folder as the file.
4. Run:
   ```
   python3 current_folder/robot.py
   ```
5. The test code at the bottom of the file will run automatically and print the results for 5 test cases: 
normal readings, numeric strings, invalid values, negative values, and boundary values (exactly 0.5m and 1m).


## 5. What did I learn from using AI?

Using AI while building this helped me:

- see how to structure a program more clearly
- Writing good comments that explain *why* the code does something, not just *what* it does.
- How to write a README file "like this one"
- It was a great aid to polish my files to make them professional.
