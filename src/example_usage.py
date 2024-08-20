from Spacecraft     import Spacecraft as SC
from planetary_data import earth
import numpy as np

ER = earth[ 'radius' ]

# Initial Conditions
sma   = 26500              # Semi-major axis
e     = 0.73               # Eccentricity
i     = 63.4 * (np.pi/180) # Inclination
raan  = 45 * (np.pi/180)   # Right Ascension of Ascending Node
aop   = 270 * (np.pi/180)  # Argument of perigee
ta    = 0                  # True Anomaly

# Construct coe array 
coes = [ sma, e, i, raan, aop, ta ]

# Create an instance of the 'Spacecraft' class
sc = SC({
    'cb'    : earth,
    'coes'  : coes,
    'tspan' : '2',
    'atol'  : 1e-6,
    'rtol'  : 1e-6
})

# Groundtracks
sc.plot_groundtrack()