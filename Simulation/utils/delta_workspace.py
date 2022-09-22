#!/usr/bin/env python3

from RobotDelta import *
from math import pi


def main():
    np.set_printoptions(precision=3, suppress=True)

    robot = RobotDelta(np.array([0.15, 0.035, 0.15, 0.50]))
    robot.ws_lim = np.array([[-pi/12, pi/2]]*3)
    robot.ws_division = 10
    robot.show(ws=True)


if __name__ == "__main__":
    main()
