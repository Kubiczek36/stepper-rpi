#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 19:54:58 2021

@author: pi
"""

from stepper import stepper as stp
import time
import numpy as np
#import matplotlib.pyplot as plt

motor = stp(2,3,4,17)

motor.addMotor(14,15,18,23)
for i in range(2**9):
    motor.halfstep(1)

motor = stp(14,15,18,23)

motor.addMotor(2,3,4,17)
for i in range(20):
    motor.halfstep(1)
    motor.halfstep(0)

#motor2 = stp(14,15,18,23)


def test(x):
    cas = time.time()
    for i in range(20):
        motor.turnDeg(x), motor2.turnDeg(-x)
        motor.turnDeg(-x), motor2.turnDeg(x)
    return (time.time() - cas)

degs = [2.8, 4.4, 5.5, 7, 10, 15, 20]
degs = [1]
casy = np.empty([len(degs), 1])

#for i in range(len(degs)):
#    casy[i] = test(degs[i])
#    print("uhel", degs[i], "dokončen. Perioda:", casy[i]/20, "frekvence:", 20/casy[i])
#
#plt.plot(degs, casy)

#motor.end()

for i in range(256):
    motor.halfstep()
    motor2.halfstepAnti()
    
# =============================================================================
# Pro příště:
# - napsat třidu pro dva a obecně n motorů, která bude fungovat bez zpoždění.
# =============================================================================
