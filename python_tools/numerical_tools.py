'''
Numerical tools
'''

# Third-party Libraries
import numpy as np


def R1(angle):
        '''
        Returns DCM for single rotation about the first coordinate axis
        '''
        return np.array([
                [ 1,        0,              0       ],
                [ 0,  np.cos(angle),  np.sin(angle) ],
                [ 0, -np.sin(angle),  np.cos(angle) ]        
        ])
    
def R2(angle):
        '''
        Returns DCM for single rotation about the second coordinate axis
        '''
        return np.array([
                [  np.cos(angle),  0,  np.sin(angle) ],
                [        0,        1,        0       ],
                [ -np.sin(angle),  0,  np.cos(angle) ]
        ])

def R3(angle):
        '''
        Returns DCM for single rotation about the third coordinate axis
        '''
        return np.array([
                [  np.cos(angle),  np.sin(angle),  0 ],
                [ -np.sin(angle),  np.cos(angle),  0 ],
                [        0,             0,         1 ]
        ])