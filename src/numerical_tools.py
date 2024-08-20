'''
Numerical tools
'''

# Third-party Libraries
import numpy as np


def R1(angle, deg = False):
        '''
        Returns DCM for single rotation about the first coordinate axis
        '''
        if deg == True:
                angle *= np.pi/180
                
        return np.array([
                [ 1,        0,              0       ],
                [ 0,  np.cos(angle),  np.sin(angle) ],
                [ 0, -np.sin(angle),  np.cos(angle) ]        
        ])
    
def R2(angle, deg = False):
        '''
        Returns DCM for single rotation about the second coordinate axis
        '''
        if deg == True:
                angle *= np.pi/180

        return np.array([
                [  np.cos(angle),  0,  np.sin(angle) ],
                [        0,        1,        0       ],
                [ -np.sin(angle),  0,  np.cos(angle) ]
        ])

def R3(angle, deg = False):
        '''
        Returns DCM for single rotation about the third coordinate axis
        '''
        if deg == True:
                angle *= np.pi/180

        return np.array([
                [  np.cos(angle),  np.sin(angle),  0 ],
                [ -np.sin(angle),  np.cos(angle),  0 ],
                [        0,             0,         1 ]
        ])

def norm( vec ):
        '''
        Returns norm of input vector
        '''
        return np.linalg.norm( vec )