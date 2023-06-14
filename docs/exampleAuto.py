def driveForward(Command):
  def execute():
    drivetrain.drive(1.0, 0.0)
  def end():
    drivetrain.drive(0.0,0.0) #stop
  def isDone():
    return drivetrain.getDistance() > 1.0 # 1 ft

def armRaise(Command):
  def execute():
    arm.set(1.0)
  def end():
    arm.set(0.0)
  def isDone():
    return arm.getDistance() > 0.25 # 1 ft




autoSequence = driveForward().andThen(armRaise().withTimeout(0.5))


