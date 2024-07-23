from Spacecraft     import Spacecraft as SC
from planetary_data import earth
import math              as m
import matplotlib.pyplot as plt

# Initial Conditions
sma   = earth[ 'radius' ] + 758.63 # Semi-major axis
e     = 0                          # Eccentricity
i     = 98.43*(m.pi/180)           # Inclination
raan  = 0                          # Right Ascension of Ascending Node
omega = 0                          # Argument of perigee
ta    = 0                          # True Anomaly

# Construct coe array 
coes = [ sma, e, i, raan, omega, ta ]

# Create an instance of the 'Spacecraft' class
sc = SC({
    'cb'    : earth,
    'coes'  : [ earth[ 'radius' ] + 758.63, 0, 98.43*(m.pi/180), 0, 0, 0],
    'tspan' : '1',
    'atol'  : 1e-9,
    'rtol'  : 1e-9
})

# Plot orbit
ax = plt.figure().add_subplot(projection='3d')
ax.plot(
    sc.states[ :, 0 ], 
    sc.states[ :, 1 ], 
    sc.states[ :, 2 ], 
    label = 'orbit'
)
ax.legend()

plt.show()