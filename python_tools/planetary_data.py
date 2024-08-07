'''
Planetary Data Library

Note: Units are in KM-S for each planet dictionary.
'''

# gravitational constant
G_meters = 6.67430e-11       # m**3 / kg / s**2
G        = G_meters * 10**-9 # km**3/ kg / s**2

# planet dictionaries

mercury = {
		'name'            : 'Mercury',
		'ID'              : 199,
		'mass'            : 0.330103e24,
		'mu'              : 0.330103e24 * G,
		'radius'          : 2440.53,
		'J2'     		  : 50.3e-6,
		'sma'             : 57.91e6,  
		'SOI'             : 1.1241e5, 
		'cmap'            : 'Wistia',
		'traj_color'      : 'y'
		}

venus = {
		'name'            : 'Venus',
		'ID'              : 299,
		'mass'            : 4.867e24,
		'mu'              : 3.2485859200000006E+05,
		'radius'          : 6051.8,
		'J2'			  : 4.458e-6,
		'sma'             : 108.209e6,  
		'SOI'             : 617183.2511,
		'cmap'            : 'Wistia',
		'traj_color'      : 'y'
		}

earth = {
		'name'            : 'Earth',
		'ID'              : 399,
		'mass'            : 5.972e24,
		'mu'              : 5.972e24 * G,
		'radius'          : 6378.0,
		'J2'              : 1.082626683e-3, # WGS84
		'sma'             : 149.596e6,
		'SOI'             : 926006.6608,
		'cmap'            : 'Blues',
		'traj_color'      : 'b'
		}

mars = {
		'name'            : 'Mars',
		'ID'              : 499,
		'mass'            : 6.39e23,
		'mu'              : 4.282837362069909E+04,
		'radius'          : 3397.0,
		'J2'			  : 1960.45e-6,
		'sma'             : 227.923e6,
		'SOI'             : 0.578e6,  
		'cmap'            : 'Reds',
		'traj_color'      : 'r'
		}

jupiter = {
		'name'            : 'Jupiter',
		'ID'              : 599,
		'mass'            : 1.898e27,
		'mu'              : 1.26686e8,
		'radius'          : 71490.0,
		'J2'              : 14736e-6,
		'sma'             : 778.570e6, 
		'SOI'             : 48.2e6,  
		'traj_color'      : 'C3'
}

saturn = {
		'name'            : 'Saturn',
		'ID'              : 699,
		'mass'            : 1.8981e26,
		'mu'              : 1.8981e26 * G,
		'radius'          : 60270,
		'J2'			  : 16298e-6,
		'sma'             : 778.6e6,
		'SOI'             : 54.787e6,
		'traj_color'      : 'C3'
}

uranus = {
		'name'            : 'Uranus',
		'ID'              : 799,
		'mass'            : 8.6811e24,
		'mu'              : 8.6811e24 * G,
		'radius'          : 25560,
		'J2'		      : 3343.43e-6, 
		'sma'             : 2872e6, 
		'SOI'             : 5.1785e7, 
		'traj_color'      : 'C3'
}

neptune = {
		'name'            : 'Neptune',
		'ID'              : 899,
		'mass'            : 1.0241e25,
		'mu'              : 1.0241e25 * G,
		'radius'          : 24760,   
		'J2'			  : 4311e-6,
		'sma'             : 4495e6, 
		'SOI'             : 8.6589e7, 
		'traj_color'      : 'C3'
}

pluto = {
		'name'            : 'Pluto',
		'ID'              : 999,
		'mass'            : 1.3029e21,
		'mu'              : 1.3029e21 * G,
		'radius'          : 1188,   # km
		'sma'             : 5.90638e9, # km
		'traj_color'      : 'C3'
} 

moon = {
		'name'            : 'Moon',
		'ID'              : 301,
		'mass'            : 5.972e24,
		'mu'              : 5.972e24 * G,
		'radius'          : 1737.4,
		'J2'              : 1.081874e-3,
		'sma'             : 149.596e6, # km
		'SOI'             : 926006.6608, # km
		'cmap'            : 'Blues',
		'traj_color'      : 'b'
		}

io = {
		'name'            : 'Io',
		'ID'              : 501,
		'mass'            : 1.898e27,
		'mu'              : 5.959916033410404E+03,
		'radius'          : 1821.6,  
		'traj_color'      : 'C1'
}



europa = {
		'name'            : 'Europa',
		'ID'              : 502,
		'mu'              : 3.202738774922892E+03,
		'radius'          : 1560.8,  
		'traj_color'      : 'C2'
}

ganymede = {
		'name'            : 'Ganymede',
		'ID'              : 503,
		'mu'              : 9.887834453334144E+03,
		'radius'          : 2631.2, 
		'traj_color'      : 'C3'
}

callisto = {
		'name'            : 'Callisto',
		'ID'              : 504,
		'mu'              : 7.179289361397270E+03,
		'radius'          : 2410.3,
		'traj_color'      : 'C4'
}

sun = {
	'name'            : 'Sun',
	'mass'            : 1.989e30,
	'mu'              : 1.3271244004193938E+11,
	'radius'          : 695510.0,
	'cmap'            :'gist_heat'
}

# list of planet dictionaries
bodies = [
	venus, earth, moon, mars, 
	jupiter, io, europa, ganymede, callisto,
	saturn, sun ]

# Add diameter entry for each body
for body in bodies:
	body[ 'diameter' ]    = body[ 'radius' ] * 2 # [km]