import wpilib


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        print("It's Init Time")
    
    def robotPeriodic(self):
        print("Periodic")
        
    def teleopPeriodic(self):
        print("teleop")
        
        
if __name__ == '__main__':
    wpilib.run(MyRobot)