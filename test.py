#! /usr/bin/python3

# -*- coding: utf-8 -*-

import os, time, threading, subprocess
import requests, logging, random
import matplotlib as mpl
import matplotlib.pyplot as plt, mpld3

fig = plt.figure()

plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)

print(mpld3.fig_to_html(fig))

