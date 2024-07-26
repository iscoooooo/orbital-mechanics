from Spacecraft     import Spacecraft as SC
from planetary_data import earth
import math             as m

# Initial Conditions
sma   = earth[ 'radius' ] + 5000 # Semi-major axis
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
    'coes'  : coes,
    'tspan' : '1',
    'atol'  : 1e-9,
    'rtol'  : 1e-9
})

# Show 3D plot
sc.plot3( 'Molniya', 'b' )