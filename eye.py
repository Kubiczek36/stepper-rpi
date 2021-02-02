#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 19:15:18 2021

@author: pi
"""

import numpy as np


class matice:
    def __init__(self):
        self.a = np.eye(3)
    def show(self):
        print(self.a)
    def nasobek(self, n):
        self.a *=n