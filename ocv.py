__author__ = 'VM_PRL'

import cv2
import matplotlib.pyplot as plt
import numpy as np


def set_data(xdata, ydata,  num_of_files):
    e1 = cv2.getTickCount()  # get start time

    plt.figure('intensity plot')
    plt.imshow(ydata, cmap='binary')
    plt.show(block=False)


    e2 = cv2.getTickCount()  # get stop time
    time = (e2 - e1) / cv2.getTickFrequency()  # evaluate execution time
    print time