# Helper functions to assist with MRI rendering (soooo helpful... right?)
import numpy as np
from OpenGL.GL import *

def normalize_mri_data(data):
    # Normalize data so that it fits between 0 and 1 (i think that's right)
    max_val = np.max(data)  # find da max
    min_val = np.min(data)  # and the min
    return (data - min_val) / (max_val - min_val)

def generate_brain_mesh(data):
    # generate brain mesh from data (not sure if this works lol)
    vertices = []
    for z in range(data.shape[2]):
        for x in range(data.shape[0]):
            for y in range(data.shape[1]):
                intensity = data[x, y, z]
                if intensity > 0:  # only keep the 'bright' parts of the brain
                    vertices.append((x, y, z))
    return vertices  # give bak vertices for OpenGL
