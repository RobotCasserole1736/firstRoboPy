import math
from wpimath.units import inchesToMeters
from wpimath.system.plant import DCMotor
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics
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
WHEEL_BASE_HALF_WIDTH_M = inchesToMeters(23.75 / 2.0)
WHEEL_BASE_HALF_LENGTH_M = inchesToMeters(23.75 / 2.0)

# Additional distance from the wheel contact patch out to the edge of the bumper
BUMPER_THICKNESS_M = inchesToMeters(2.5)

# Total mass includes robot, battery, and bumpers
# more than the "weigh-in" weight
ROBOT_MASS_KG = lbsToKg(140)

# Model the robot's moment of intertia as a square slab
# slightly bigger than wheelbase with axis through center
ROBOT_MOI_KGM2 = (
    1.0 / 12.0 * ROBOT_MASS_KG * math.pow((WHEEL_BASE_HALF_WIDTH_M * 2.2), 2) * 2
)

# SDS MK4i Swerve Module Ratios
# See https://www.swervedrivespecialties.com/products/mk4i-swerve-module?variant=39598777172081
WHEEL_GEAR_RATIO_L1 = 8.41
WHEEL_GEAR_RATIO_L2 = 6.75
WHEEL_GEAR_RATIO_L2 = 6.12
AZMTH_GEAR_RATIO = 12.8

### CHANGE THIS DEPENDING ON WHICH MODULE GEAR RATIO IS INSTALLED
WHEEL_GEAR_RATIO = WHEEL_GEAR_RATIO_L1

# carpet/roughtop interface fudge factor
# This accounts for the fact that roughtop tread
# sinks into the carpet slightly. Determined empirically
# by driving the robot a known distance, seeing the measured distance in software,
# and adjusting this factor till the measured distance matches known
# Might have to be different for colson wheels?
WHEEL_FUDGE_FACTOR = 0.9238

# Nominal 4-inch diameter swerve drive wheels
# https:#www.swervedrivespecialties.com/collections/mk4i-parts/products/billet-wheel-4d-x-1-5w-bearing-bore
WHEEL_RADIUS_IN = 4.0 / 2.0 * WHEEL_FUDGE_FACTOR


# Utility conversion functions to go between drivetrain "linear" measurements and wheel motor rotational measurements
def dtLinearToMotorRot(lin):
    # lin - meters per second at wheel contact patch
    # return - radians per second of motor shaft
    return lin / (inchesToMeters(WHEEL_RADIUS_IN)) * WHEEL_GEAR_RATIO


def dtMotorRotToLinear(rot):
    # rot - radians per second of motor shaft
    # return = meters per second at wheel contact patch
    return rot * (inchesToMeters(WHEEL_RADIUS_IN)) / WHEEL_GEAR_RATIO


# Drivetrain Performance Mechanical limits
# Nominal calculations (ideal)
MAX_DT_MOTOR_SPEED_RPS = DCMotor.NEO(1).freeSpeed
MAX_DT_LINEAR_SPEED = MAX_DT_MOTOR_SPEED_RPS / WHEEL_GEAR_RATIO * in2m(WHEEL_RADIUS_IN)
# Fudged max expected performance
MAX_FWD_REV_SPEED_MPS = MAX_DT_LINEAR_SPEED * 0.98  # fudge factor due to gearbox losses
MAX_STRAFE_SPEED_MPS = MAX_DT_LINEAR_SPEED * 0.98  # fudge factor due to gearbox losses
MAX_ROTATE_SPEED_RAD_PER_SEC = deg2Rad(
    360.0
)  # Fixed at the maximum rotational speed we'd want.
# Accelerations - also a total guess
MAX_TRANSLATE_ACCEL_MPS2 = (
    MAX_FWD_REV_SPEED_MPS / 0.50
)  # 0-full time of 0.5 second - this is a guestimate
MAX_ROTATE_ACCEL_RAD_PER_SEC_2 = (
    MAX_ROTATE_SPEED_RAD_PER_SEC / 0.25
)  # 0-full time of 0.25 second - this is a guestaimate


# Mechanical mounting offsets of the encoder & magnet within the shaft
# Must be updated whenever the module is reassembled
# Procedure:
# 0 - Put the robot up on blocks.
# 1 - Reset all these values to 0, deploy code
# 2 - Pull up dashboard with encoder readings (in radians)
# 3 - Using a square, twist the modules by hand until they are aligned with the robot's chassis
# 4 - Read out the encoder readings for each module, put them here
# 5 - Redeploy code, verify that the  encoder readings are correct as each module is manually rotated
FL_ENCODER_MOUNT_OFFSET_RAD = deg2Rad(-37.86)
FR_ENCODER_MOUNT_OFFSET_RAD = deg2Rad(136.3)
BL_ENCODER_MOUNT_OFFSET_RAD = deg2Rad(59.97)
BR_ENCODER_MOUNT_OFFSET_RAD = deg2Rad(-64.44)


# Module Indices (for ease of array manipulation)
FL = 0
FR = 1
BL = 2
BR = 3

# Array of translations from robot's origin (center bottom, on floor) to the module's contact patch with the ground
robotToModuleTranslations = []
robotToModuleTranslations.append(
    Translation2d(WHEEL_BASE_HALF_WIDTH_M, WHEEL_BASE_HALF_LENGTH_M)
)
robotToModuleTranslations.append(
    Translation2d(WHEEL_BASE_HALF_WIDTH_M, -WHEEL_BASE_HALF_LENGTH_M)
)
robotToModuleTranslations.append(
    Translation2d(-WHEEL_BASE_HALF_WIDTH_M, WHEEL_BASE_HALF_LENGTH_M)
)
robotToModuleTranslations.append(
    Translation2d(-WHEEL_BASE_HALF_WIDTH_M, -WHEEL_BASE_HALF_LENGTH_M)
)

# WPILib Kinematics object
kinematics = SwerveDrive4Kinematics(
    robotToModuleTranslations[FL],
    robotToModuleTranslations[FR],
    robotToModuleTranslations[BL],
    robotToModuleTranslations[BR],
)
