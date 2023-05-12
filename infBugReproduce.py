import wpilib
import ntcore

class MyRobot(wpilib.TimedRobot):
    def robotInit(self): 
        table = ntcore.NetworkTableInstance.getDefault().getTable("TestTable")
        
        topic = table.getDoubleTopic("testVal")
        self.pub = topic.publish(ntcore.PubSubOptions(
                                    sendAll=False, keepDuplicates=False))
        self.pub.setDefault(0.0)

        propValDes = float('-inf')
        topic.setProperty("doesntWork", propValDes)

        propValAct = topic.getProperty("doesntWork")
        print(propValDes)
        print(propValAct)

    def robotPeriodic(self):
        self.pub.set(wpilib.Timer.getFPGATimestamp())

if __name__ == '__main__':
    wpilib.run(MyRobot)