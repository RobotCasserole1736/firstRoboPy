# pylint: disable-all


from wpilib import getDeployDirectory
import logging


def test_deployDirectory():
    with open("deploydirlog.txt", "w") as f:
        deployDir = getDeployDirectory()
        f.write(deployDir)
