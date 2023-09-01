import math
from wpimath.units import inchesToMeters
from wpimath.system.plant import DCMotor
from utils.units import lbsToKg
from utils.units import deg2Rad
from utils.units import in2m

"""
Defines the physical dimensions and characteristics of the drivetrain
"""

###################################################################
# Physical dimensions and mass distribution

# Wheel base half width: Distance from the center of the frame rail
# out to the center of the "contact patch" where the wheel meets the ground
WHEEL_BASE_HALF_WIDTH_M = inchesToMeters(23.75/2.0)
WHEEL_BASE_HALF_LENGTH_M = inchesToMeters(23.75/2.0)

# Additional distance from the wheel contact patch out to the edge of the bumper
BUMPER_THICKNESS_M = inchesToMeters(2.5)

# Total mass includes robot, battery, and bumpers
# more than the "weigh-in" weight
ROBOT_MASS_kg = lbsToKg(140)

# Model the robot's moment of intertia as a square slab 
# slightly bigger than wheelbase with axis through center
ROBOT_MOI_KGM2 = 1.0/12.0 * ROBOT_MASS_kg *  math.pow((WHEEL_BASE_HALF_WIDTH_M*2.2),2) * 2 

# SDS MK4i Swerve Modules 
# See https://www.swervedrivespecialties.com/products/mk4i-swerve-module?variant=39598777172081
WHEEL_GEAR_RATIO = 6.75 #L2 gearing - change this if the module speed is changed
AZMTH_GEAR_RATIO = 12.8

# carpet/roughtop interface fudge factor
# This accounts for the fact that roughtop tread
# sinks into the carpet slightly. Determined empirically
# by driving the robot a known distance, seeing the measured distance in software,
# and adjusting this factor till the measured distance matches known
WHEEL_FUDGE_FACTOR = 0.9238 

# Nominal 4-inch diameter swerve drive wheels
# https:#www.swervedrivespecialties.com/collections/mk4i-parts/products/billet-wheel-4d-x-1-5w-bearing-bore
WHEEL_RADIUS_IN = 4.0/2.0 * WHEEL_FUDGE_FACTOR 

# Utility conversion functions to go between drivetrain "linear" measurements and wheel motor rotational measurements
def dtLinearToMotorRot_rad(linear_m_in):
    return linear_m_in / (inchesToMeters(WHEEL_RADIUS_IN)) * WHEEL_GEAR_RATIO

def dtMotorRotToLinear_m(motorRot_rad_in):
    return motorRot_rad_in * (inchesToMeters(WHEEL_RADIUS_IN)) / WHEEL_GEAR_RATIO


# Drivetrain Performance Mechanical limits
# Nominal calculations (ideal)
MAX_DT_MOTOR_SPEED_RPS = DCMotor.NEO(1).freeSpeed
MAX_DT_LINEAR_SPEED = MAX_DT_MOTOR_SPEED_RPS / WHEEL_GEAR_RATIO * in2m(WHEEL_RADIUS_IN)
# Fudged max expected performance 
MAX_FWD_REV_SPEED_MPS = MAX_DT_LINEAR_SPEED * 0.98 #fudge factor due to gearbox losses
MAX_STRAFE_SPEED_MPS = MAX_DT_LINEAR_SPEED * 0.98  #fudge factor due to gearbox losses
MAX_ROTATE_SPEED_RAD_PER_SEC = deg2Rad(360.0) #Fixed at the maximum rotational speed we'd want.
# Accelerations - also a total guess
MAX_TRANSLATE_ACCEL_MPS2 = MAX_FWD_REV_SPEED_MPS/0.50 #0-full time of 0.5 second - this is a guestimate
MAX_ROTATE_ACCEL_RAD_PER_SEC_2 = MAX_ROTATE_SPEED_RAD_PER_SEC/.25 #0-full time of 0.25 second - this is a guestaimate