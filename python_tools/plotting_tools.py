'''
Plotting tools
'''

import os
import csv
import numpy                as     np 
import matplotlib.pyplot    as     plt
from   matplotlib           import cm
plt.style.use( 'dark_background' )

time_handler = {
	'seconds': { 'coeff': 1.0,        'xlabel': 'Time (seconds)' },
	'hours'  : { 'coeff': 3600.0,     'xlabel': 'Time (hours)'   },
	'days'   : { 'coeff': 86400.0,    'xlabel': 'Time (days)'    },
	'years'  : { 'coeff': 31536000.0, 'xlabel': 'Time (years)'   }
}

dist_handler = {
	'km'    : 1.0,
	'ER'    : 1 / 6378.0,
	'JR'    : 1 / 71490.0,
	'AU'    : 6.68459e-9,
	r'$\dfrac{km}{s}$': 1.0
}

COLORS = [ 
	'm', 'deeppink', 'chartreuse', 'w', 'springgreen', 'peachpuff',
	'white', 'lightpink', 'royalblue', 'lime', 'aqua' ] * 100

EARTH_COASTLINES = os.path.join(
    os.path.dirname( __file__ ),
    os.path.join( '..', 'data', 'earth_coastlines.csv' )
)


def plot_3d( positions, planet_radius, plt_label = 'orbit', traj_color = 'red', figsize = ( 10, 10 ) ):

    # Create figure and add 3d subplot
    fig = plt.figure( figsize = figsize )
    ax  = fig.add_subplot( 111, projection = '3d' )

    # Draw the planet
    u, v = np.mgrid[ 0:2*np.pi:100j, 0:np.pi:100j  ]
    x = planet_radius * np.cos( u ) * np.sin( v ) 
    y = planet_radius * np.sin( u ) * np.sin( v ) 
    z = planet_radius * np.cos( v )

    ax.plot_surface( x, y, z, rstride = 5, cstride = 5, cmap = cm.Blues, zorder = 0 )

    # Plot trajectory 
    ax.plot(
        positions[ :, 0 ],
        positions[ :, 1 ],
        positions[ :, 2 ],
        label = plt_label,
        color = traj_color
    )

    # Set an equal aspect ratio
    ax.set_aspect( 'equal' )

    if plt_label:
        ax.legend()

    plt.show()


def plot_groundtracks( coords ):
    # List to hold latitude and longitude data
    coast_latitudes = []
    coast_longitudes = []

    # Load Earth coastlines
    with open( EARTH_COASTLINES, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            longitude, latitude = map(float, row)
            coast_longitudes.append(longitude)
            coast_latitudes.append(latitude)

    # Set figure size
    fig = plt.figure(figsize=(18, 9))
    ax = fig.add_subplot()

    # Plot groundtracks with wrap-around handling
    prev_lon = coords[0, 0]
    segment_lat = [coords[0, 1]]
    segment_lon = [coords[0, 0]]

    for lon, lat in coords[1:]:
        if abs(lon - prev_lon) > 180:
            # Detected a wrap-around, plot current segment
            ax.plot(segment_lon, np.array(segment_lat))  # Use a fixed color 'b' (blue)
            # Start a new segment
            segment_lat = [lat]
            segment_lon = [lon]
        else:
            # Continue the current segment
            segment_lat.append(lat)
            segment_lon.append(lon)
        prev_lon = lon

    # Plot the last segment
    ax.plot(segment_lon, np.array(segment_lat))  # Use a fixed color 'b' (blue)

    # Mark start and end points
    ax.scatter(coords[0, 0], coords[0, 1], color='g', s=100, label='Start')
    ax.scatter(coords[-1, 0], coords[-1, 1], color='r', s=100, label='End')

    # Plot coastlines
    ax.scatter(coast_longitudes, coast_latitudes, s=0.1, color='m')

    # Set axes limits
    ax.set_xlim((-180, 180))
    ax.set_ylim((-90, 90))
    ax.set_aspect('auto')
    ax.grid( True, 'major', linestyle = 'dotted' )
    ax.set_xticks( range( -180, 200, 20 ) )
    ax.set_yticks( range( -90, 100, 10 ) )

    # Plot labels
    ax.set_xlabel( r'Longitude (degrees $^\circ$)', fontsize = 14 )
    ax.set_ylabel( r'Latitude (degrees $^\circ$)', fontsize = 14  )
    ax.set_title( 'Spacecraft groundtrack', fontsize = 14 )

    plt.legend()
    plt.show()

def plot_coes( times, coes, args = {} ):
    _args = {
        'figsize'   : ( 18, 9 ),
        'labels'    : [ '' ] * len( coes ),
        'lws'       : 1,
        'color'     : 'm',
        'grid'      : True,
        'title'     : 'COEs',
        'title_fs'  : 25,
        'wspace'    : 0.3,
        'time_unit' : 'seconds',
        'show'      : False,
        'filename'  : False,
        'dpi'       : 300,
        'legend'    : True
    }

    for key in args.keys():
        _args[ key ] = args[ key ]

    _args[ 'xlabel' ]     = time_handler[ _args[ 'time_unit' ] ][ 'xlabel' ]
    _args[ 'time_coeff' ] = time_handler[ _args[ 'time_unit' ] ][ 'coeff'  ]

    times = times / _args[ 'time_coeff' ]

    fig, ( ( ax0, ax1, ax2 ), ( ax3, ax4, ax5 ) ) = plt.subplots(
        2, 3,
        figsize = _args[ 'figsize' ]
    )

    fig.suptitle( _args[ 'title' ], fontsize = _args[ 'title_fs'] )

    # True anomaly
    n = 0
    for coe in coes:
        ax0.plot(
            times, coe[ :, 5 ], _args[ 'color' ], label = _args[ 'labels' ][ n ] 
        )
        n += 1
    ax0.set_ylabel( 'True Anomaly $(deg)$' )
    ax0.grid( linestyle = 'dotted' )

    # semi-major axis
    n = 0
    for coe in coes:
        ax3.plot(
            times, coe[ :, 0 ], _args[ 'color' ], label = _args[ 'labels' ][ n ] 
        )
        n += 1
    ax3.set_ylabel( 'Semi-Major Axis $(km)$' )
    ax3.set_xlabel( _args[ 'xlabel' ] )
    ax3.grid( linestyle = 'dotted' )

    # eccentricity
    n = 0
    for coe in coes:
        ax1.plot(
            times, coe[ :, 1 ], _args[ 'color' ], label = _args[ 'labels' ][ n ] 
        )
        n += 1
    ax1.set_ylabel( 'Eccentricity' )
    ax1.grid( linestyle = 'dotted' )

    # inclination
    n = 0
    for coe in coes:
        ax4.plot(
            times, coe[ :, 2 ], _args[ 'color' ], label = _args[ 'labels' ][ n ] 
        )
        n += 1
    ax4.set_ylabel( 'Inclination $(deg)$' )
    ax4.set_xlabel( _args[ 'xlabel' ] )
    ax4.grid( linestyle = 'dotted' )

    # argument of periapsis
    n = 0
    for coe in coes:
        ax2.plot(
            times, coe[ :, 4 ], _args[ 'color' ], label = _args[ 'labels' ][ n ] 
        )
        n += 1
    ax2.set_ylabel( 'Argument of Periapsis $(deg)$' )
    ax2.grid( linestyle = 'dotted' )

    # right ascension of ascending node
    n = 0
    for coe in coes:
        ax5.plot(
            times, coe[ :, 3 ], _args[ 'color' ], label = _args[ 'labels' ][ n ] 
        )
        n += 1
    ax5.set_ylabel( 'RAAN $(deg)$' )
    ax5.set_xlabel( _args[ 'xlabel' ] )
    ax5.grid( linestyle = 'dotted' )

    plt.subplots_adjust( wspace = _args[ 'wspace' ] )

    if _args[ 'show' ]:
        plt.show()
    
    if _args[ 'filename' ]:
        plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )

    plt.close()