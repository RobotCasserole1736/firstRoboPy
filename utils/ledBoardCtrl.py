

from wpilib import DigitalOutput, Joystick, SmartDashboard, Spark


class LEDBoardCtrl():
    def __init__(self, PWMPort):
        self.out = Spark(PWMPort)
        self.ctrlJoy = Joystick(0)

    def update(self):
        self.out.set(self.ctrlJoy.getRawAxis(0))



    