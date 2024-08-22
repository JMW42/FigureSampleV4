import numpy as np
import pandas as pd
from PIL import Image, ImageTk


LIB_VERSION = "0.1"

def color_norm(color, rcolor, ncweight):
    """ The colornorm used by the software to calculate the vectorial distance between different colors"""
    res = 0

    for i in range(4):
        res += np.abs(rcolor[i] - color[i])

    res = res / (255*np.sum(ncweight))
    return res



def calculate_color_norm(img_data, sframe, rcolor, ncweight):
    """ calculates the color norm picture of the given data with specified arguments"""
    res = np.ones([img_data.shape[0], img_data.shape[1]])

    
    for x in range(img_data.shape[1]):
        # sframe = (x1, y1, x2, y2)
        if x < sframe[0] or x > sframe[2]: continue
 
        for y in range(img_data.shape[0]):
            if y < sframe[1] or y > sframe[3]: continue
            color = (img_data[y][x][0], img_data[y][x][1], img_data[y][x][2], img_data[y][x][3])
            res[y][x] = color_norm(color, rcolor, ncweight)


    print(f"selected: {res.shape}")
    return res


def evaluate_norm(norm_data, nfilter):
    """ evaluates the given norm data and returns an tuple with two arrays containing the inxes lists (x, y)"""
    xarr = []
    yarr = []
    vals = []

    for x in range(norm_data.shape[1]):
        row = norm_data[:, x]
        y = np.argmin(row)
        val = row[y]

        if( val > nfilter[0] and val < nfilter[1]):
            xarr.append(x)
            yarr.append(y)
            vals.append(val)

    return xarr, yarr, vals

