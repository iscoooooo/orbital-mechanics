'''
Plotting tools
'''

import os
import csv
import numpy                as     np 
import matplotlib.pyplot    as     plt
from   matplotlib           import cm
from   planetary_data       import earth
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


def plot_3d( rs, args, vectors = [] ):
    _args = {
        'figsize'       : ( 10, 8 ),
        'labels'        : [ '' ] * len( rs ),
        'colors'        : COLORS[ : ],
        'traj_lws'      : 3,
        'dist_unit'     : 'km',
        'cb_radius'     : earth[ 'radius' ],
        'cb_SOI'        : None,
        'cb_SOI_color'  : 'c',
        'cb_SOI_alpha'  : 0.7,
        'cb_axes'       : True,
        'cb_axes_mag'   : 2,
        'cb_cmap'       : cm.Blues,
        'cb_axes_color' : 'w',
        'axes_mag'      : 0.8,
        'axes_custom'   : None,
        'title'         : 'Trajectories',
        'legend'        : True,
        'axes_no_fill'  : True, 
        'hide_axes'     : False,
        'azimuth'       : False,
        'elevation'     : False,
        'show'          : False,
        'filename'      : False,
        'dpi'           : 300,
        'vector_colors' : [ '' ] * len( vectors ),
        'vector_labels' : [ '' ] * len( vectors ),
        'vector_texts'  : False
    }

    for key in args.keys():
        _args[ key ] = args[ key ] 
 
    # Create figure and add 3d subplot
    fig = plt.figure( figsize = _args[ 'figsize' ] )
    ax  = fig.add_subplot( 111, projection = '3d' )

    # Plot central body
    _args[ 'cb_radius' ] *= dist_handler[ _args[ 'dist_unit' ] ]

    _u, _v = np.mgrid[ 0:2*np.pi:100j, 0:np.pi:100j  ]
    _x = _args[ 'cb_radius' ] * np.cos( _u ) * np.sin( _v ) 
    _y = _args[ 'cb_radius' ] * np.sin( _u ) * np.sin( _v ) 
    _z = _args[ 'cb_radius' ] * np.cos( _v )

    ax.plot_surface( _x, _y, _z, rstride = 5, cstride = 5, cmap = cm.Blues, zorder = 0 )

    # Plot trajectories

    max_val = 0
    n       = 0

    for r in rs:
        _r = r.copy() * dist_handler[ _args[ 'dist_unit' ] ] 

        ax.plot(
            _r[ :, 0 ], _r[ :, 1 ], _r[ :, 2 ],
            color = _args[ 'colors' ][ n ],
            label = _args[ 'labels' ][ n ],
            linewidth = _args[ 'traj_lws' ],
            zorder = 10
        )
        ax.plot(
            [ _r[ 0, 0 ] ], [ _r[ 0, 1 ] ], [ _r[ 0, 2 ]] ,
            'o', color = _args[ 'colors' ][ n ]
        )

        # consider the orbit groundtrack on the planet in the future

        max_val = max( [ _r.max(), max_val ] )
        n += 1

    # Plot vectors that are passed in as a dictionary type
    for vector in vectors:
        ax.quiver( 
            0, 0, 0,
            vector[ 'r' ][ 0 ], vector[ 'r' ][ 1 ], vector[ 'r' ][ 2 ],
            color = vector[ 'color' ], label = vector[ 'label' ]
        )

        if _args[ 'vector_texts' ]:
            vector[ 'r' ] *= _args[ 'vector_texts_scale' ]
            ax.text( 
                vector[ 'r' ][ 0 ], vector[ 'r' ][ 1 ], vector[ 'r' ][ 2 ],
                label = vector[ 'label' ],
                color = vector[ 'color' ],
                length=1, scale=20, pivot='tail'
            )
    
    if _args[ 'cb_SOI' ] is not None:
        _args[ 'cb_SOI' ] *= dist_handler[ _args[ 'dist_unit' ] ]
        
        # Rescaling of the SOI relative to central body radius, for visual purposes
        _x = _args[ 'cb_SOI' ] / _args[ 'cb_radius' ]
        _y = _args[ 'cb_SOI' ] / _args[ 'cb_radius' ]
        _z = _args[ 'cb_SOI' ] / _args[ 'cb_radius' ]

        ax.plot_wireframe( _x, _y, _z,
			color = _args[ 'cb_SOI_color' ],
			alpha = _args[ 'cb_SOI_alpha' ]
        )

    if _args[ 'cb_axes' ]:
        l  = _args[ 'cb_radius' ] * _args[ 'cb_axes_mag' ]

        x, y, z = [ [ 0, 0, 0 ], [ 0, 0, 0 ], [ 0, 0, 0 ] ]
        u, v, w = [ [ l, 0, 0 ], [ 0, l, 0 ], [ 0, 0, l ] ]

        ax.quiver( x, y, z, u, v, w,
            color = _args[ 'cb_axes_color' ]          
        )

    # Set axes labels
    xlabel = 'X (%s)' % _args[ 'dist_unit' ] 
    ylabel = 'Y (%s)' % _args[ 'dist_unit' ] 
    zlabel = 'Z (%s)' % _args[ 'dist_unit' ]

    ax.set_xlabel( xlabel )
    ax.set_ylabel( ylabel )
    ax.set_zlabel( zlabel )

    # Set axes limits
    if _args[ 'axes_custom' ] is not None:
        max_val = _args[ 'axes_custom' ]
    else:
        max_val *= _args[ 'axes_mag' ]

    ax.set_xlim( [ -max_val, max_val ] )
    ax.set_ylim( [ -max_val, max_val ] )
    ax.set_zlim( [ -max_val, max_val ] )

    # Set aspect ratio
    ax.set_box_aspect( [ 1, 1, 1 ] )
    ax.set_aspect( 'auto' )

    if _args[ 'azimuth' ] is not False:
        ax.view_init( elev = _args[ 'elevation' ], azim = _args[ 'azimuth'] )
    
    if _args[ 'axes_no_fill' ]:
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
    
    if _args[ 'hide_axes' ]:
        ax.set_axis_off()

    if _args[ 'legend' ]:
        plt.legend()
    
    if _args[ 'filename' ]:
        plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
        print( 'Saved', _args[ 'filename' ] )

    if _args[ 'show' ]:
        plt.show()
    
    plt.close()

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
    fig = plt.figure( figsize=(18, 9) )
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

def plot_states( times, states, args = {} ):
    _args = {
        'figsize'   : ( 16, 8 ),
        'dist_unit' : 'km',
        'time_unit' : 'seconds',
        'lw'        : 2.5,
        'title'     : 'Spacecraft States',
        'xlim'      : None,
        'r_ylim'    : None,
        'v_ylim'    : None,
        'legend'    : True,
        'show'      : True,
        'filename'  : False,
        'dpi'       : 300
    }

    for key in args.keys():
        _args[ key ] = args[ key ]

    # Create figure and add subplots
    fig, ( ax0, ax1 ) = plt.subplots( 2, 1, figsize = _args[ 'figsize' ] )

    _args[ 'xlabel' ]     = time_handler[ _args[ 'time_unit' ] ][ 'xlabel' ]
    _args[ 'time_coeff' ] = time_handler[ _args[ 'time_unit' ] ][ 'coeff'  ]

    times  /= _args[ 'time_coeff' ]
    rnorms  = np.linalg.norm( states[ :, :3 ], axis = 1 )
    vnorms  = np.linalg.norm( states[ :, 3: ], axis = 1 )

    if _args[ 'xlim' ] is None:
        _args[ 'xlim' ] = [ 0, times[ -1 ] ]

    if _args[ 'r_ylim' ] is None:
        _args[ 'r_ylim' ] = [ states[ :, :3 ].min(), rnorms.max() ]
    
    if _args[ 'v_ylim' ] is None:
        _args[ 'v_ylim' ] = [ states[ :, 3: ].min(), vnorms.max() ]

    
    ''' Positions '''
    ax0.plot(
        times, states[ :, 0 ],
        'r', label = r'$r_x$', linewidth = _args[ 'lw' ]
    )
    ax0.plot(
        times, states[ :, 1 ],
        'g', label = r'$r_y$', linewidth = _args[ 'lw' ]
    )
    ax0.plot(
        times, states[ :, 2 ],
        'b', label = r'$r_z$', linewidth = _args[ 'lw' ]
    )
    ax0.plot(
        times, rnorms,
        'm', label = r'$r$', linewidth = _args[ 'lw' ]
    )

    ax0.grid( linestyle = 'dotted' )
    ax0.set_xlim( _args[ 'xlim' ] )
    ax0.set_ylim( _args[ 'r_ylim' ] )
    ax0.set_ylabel( r'Position $(km)$')

    ''' Velocities '''
    ax1.plot(
        times, states[ :, 3 ],
        'r', label = r'$v_x$', linewidth = _args[ 'lw' ]
    )
    ax1.plot(
        times, states[ :, 4 ],
        'g', label = r'$v_y$', linewidth = _args[ 'lw' ]
    )
    ax1.plot(
        times, states[ :, 5 ],
        'b', label = r'$v_z$', linewidth = _args[ 'lw' ]
    )
    ax1.plot(
        times, vnorms,
        'm', label = r'$v$', linewidth = _args[ 'lw' ]
    )

    ax1.grid( linestyle = 'dotted' )
    ax1.set_xlim( _args[ 'xlim' ] )
    ax1.set_ylim( _args[ 'v_ylim' ] )
    ax1.set_ylabel( r'Velocity $(\dfrac{km}{s})$')
    ax1.set_xlabel( _args[ 'xlabel' ] )


    plt.suptitle( _args[ 'title' ] )
    plt.tight_layout

    if _args[ 'legend' ]:
        ax0.legend()
        ax1.legend()

    if _args[ 'filename' ]:
        plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
        print( 'Saved', _args[ 'filename' ] )

    if _args[ 'show' ]:
        plt.show()

    plt.close()

def plot_pos( times, pos, args = {} ):
    _args = {
        'figsize'           : ( 16, 8 ),
        'dist_unit'         : 'km',
        'time_unit'         : 'seconds',
        'lw'                : 2,
        'title'             : 'Position Profile',
        'xlim'              : None,
        'ylim'              : None,
        'labelsize'         : 15,
        'legend_fontsize'   : 20,
        'legend_framealpha' : 0.3,
        'legend'            : True,
        'show'              : False,
        'filename'          : False,
        'dpi'               : 300
    }

    for key in args.keys():
        _args[ key ] = args[ key ]

    # Create figure and add subplot
    fig, ax0 = plt.subplots( 1, 1, figsize = _args[ 'figsize' ] )

    _args[ 'xlabel' ]     = time_handler[ _args[ 'time_unit'] ][ 'xlabel' ]
    _args[ 'time_coeff' ] = time_handler[ _args[ 'time_unit'] ][ 'coeff' ]

    times /= _args[ 'time_coeff' ]
    vnorms = np.linalg.norm( pos, axis = 1 )

    if _args[ 'xlim' ] is None:
        _args[ 'xlim' ] = [ 0, times[ -1 ] ]
    
    if _args[ 'ylim' ] is None:
        _args[ 'ylim' ] = [ pos.min(), vnorms.max() ]

    ax0.plot(
        times, pos[ :, 0 ],
        'r', linewidth = _args[ 'lw' ], label = r'$r_x$'      
    )
    ax0.plot(
        times, pos[ :, 1 ],
        'g', linewidth = _args[ 'lw' ], label = r'$r_y$'      
    )
    ax0.plot(
        times, pos[ :, 2 ],
        'b', linewidth = _args[ 'lw' ], label = r'$r_z$'      
    )
    ax0.plot(
        times, vnorms,
        'm', linewidth = _args[ 'lw' ], label = r'$r$'      
    )

    ax0.grid( linestyle = 'dotted' )
    ax0.set_xlim( _args[ 'xlim' ] )
    ax0.set_ylim( _args[ 'ylim' ] )
    ax0.set_xlabel( _args[ 'xlabel' ], size = _args[ 'labelsize' ] )
    ax0.set_ylabel( r'Position $(km)$', size = _args[ 'labelsize' ] )

    plt.suptitle( _args[ 'title' ] )
    plt.tight_layout()

    if _args[ 'legend' ]:
        ax0.legend( fontsize = _args[ 'legend_fontsize' ],
            loc = 'upper right', framealpha = _args[ 'legend_framealpha' ]
        )
    
    if _args[ 'filename' ]:
        plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
        print( 'Saved', _args[ 'filename' ] )

    if _args[ 'show' ]:
        plt.show()

    plt.close()

def plot_velocities( times, velocities, args = {} ):
    _args = {
        'figsize'           : ( 16, 8 ),
        'dist_unit'         : 'km',
        'time_unit'         : 'seconds',
        'lw'                : 2,
        'title'             : 'Velocity Profile',
        'xlim'              : None,
        'ylim'              : None,
        'labelsize'         : 15,
        'legend_fontsize'   : 20,
        'legend_framealpha' : 0.3,
        'legend'            : True,
        'show'              : False,
        'filename'          : False,
        'dpi'               : 300
    }

    for key in args.keys():
        _args[ key ] = args[ key ]

    # Create figure and add subplot
    fig, ax0 = plt.subplots( 1, 1, figsize = _args[ 'figsize' ] )

    _args[ 'xlabel' ]     = time_handler[ _args[ 'time_unit'] ][ 'xlabel' ]
    _args[ 'time_coeff' ] = time_handler[ _args[ 'time_unit'] ][ 'coeff' ]

    times /= _args[ 'time_coeff' ]
    vnorms = np.linalg.norm( velocities, axis = 1 )

    if _args[ 'xlim' ] is None:
        _args[ 'xlim' ] = [ 0, times[ -1 ] ]
    
    if _args[ 'ylim' ] is None:
        _args[ 'ylim' ] = [ velocities.min(), vnorms.max() ]

    ax0.plot(
        times, velocities[ :, 0 ],
        'r', linewidth = _args[ 'lw' ], label = r'$v_x$'      
    )
    ax0.plot(
        times, velocities[ :, 1 ],
        'g', linewidth = _args[ 'lw' ], label = r'$v_y$'      
    )
    ax0.plot(
        times, velocities[ :, 2 ],
        'b', linewidth = _args[ 'lw' ], label = r'$v_z$'      
    )
    ax0.plot(
        times, vnorms,
        'm', linewidth = _args[ 'lw' ], label = r'$v$'      
    )

    ax0.grid( linestyle = 'dotted' )
    ax0.set_xlim( _args[ 'xlim' ] )
    ax0.set_ylim( _args[ 'ylim' ] )
    ax0.set_xlabel( _args[ 'xlabel' ], size = _args[ 'labelsize' ] )
    ax0.set_ylabel( r'Velocity $(\dfrac{km}{s})$', size = _args[ 'labelsize' ] )

    plt.suptitle( _args[ 'title' ] )
    plt.tight_layout()

    if _args[ 'legend' ]:
        ax0.legend( fontsize = _args[ 'legend_fontsize' ],
            loc = 'upper right', framealpha = _args[ 'legend_framealpha' ]
        )
    
    if _args[ 'filename' ]:
        plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
        print( 'Saved', _args[ 'filename' ] )

    if _args[ 'show' ]:
        plt.show()

    plt.close()

def plot_altitudes( times, alts, args = {} ):
    _args = {
        'figsize'           : ( 16, 8 ),
        'labels'            : [ '' ] * len( alts ),
        'dist_unit'         : 'km',
        'time_unit'         : 'seconds',
        'colors'            : COLORS[ : ],
        'lw'                : 2,
        'title'             : 'Altitude Profile',
        'xlim'              : None,
        'ylim'              : None,
        'labelsize'         : 15,
        'legend_fontsize'   : 20,
        'legend_framealpha' : 0.3,
        'legend'            : True,
        'show'              : False,
        'filename'          : False,
        'dpi'               : 300
    }

    for key in args.keys():
        _args[ key ] = args[ key ]

    # Create figure and add subplot
    fig, ax0 = plt.subplots( 1, 1, figsize = _args[ 'figsize' ] )

    _args[ 'xlabel' ]     = time_handler[ _args[ 'time_unit'] ][ 'xlabel' ]
    _args[ 'time_coeff' ] = time_handler[ _args[ 'time_unit'] ][ 'coeff' ]

    times /= _args[ 'time_coeff' ]

    n       = 0
    min_val = 1e10
    max_val  = 0

    for alt in alts:
        ax0.plot(
            times, alt,
            color = _args[ 'colors' ][ n ],
            linewidth = _args[ 'lw' ], 
            label = _args[ 'labels'][ n ]      
        )

        min_val = min( alt.min(), min_val )
        max_val = max( alt.max(), max_val )
        n      += 1


    if _args[ 'xlim' ] is None:
        _args[ 'xlim' ] = [ 0, times[ -1 ] ]
    
    if _args[ 'ylim' ] is None:
        _args[ 'ylim' ] = [ min_val * 0.9, max_val * 1.1 ]


    ax0.grid( linestyle = 'dotted' )
    ax0.set_xlim( _args[ 'xlim' ] )
    ax0.set_ylim( _args[ 'ylim' ] )
    ax0.set_xlabel( _args[ 'xlabel' ], size = _args[ 'labelsize' ] )
    ax0.set_ylabel( r'Altitude $(km)$', size = _args[ 'labelsize' ] )

    plt.suptitle( _args[ 'title' ] )
    plt.tight_layout()

    if _args[ 'legend' ]:
        ax0.legend( fontsize = _args[ 'legend_fontsize' ],
            loc = 'upper right', framealpha = _args[ 'legend_framealpha' ]
        )
    
    if _args[ 'filename' ]:
        plt.savefig( _args[ 'filename' ], dpi = _args[ 'dpi' ] )
        print( 'Saved', _args[ 'filename' ] )

    if _args[ 'show' ]:
        plt.show()

    plt.close()

def plot_coes( times, coes, args = {} ):
    _args = {
        'figsize'   : ( 18, 9 ),
        'labels'    : [ '' ] * len( coes ),
        'lws'       : 1,
        'color'     : 'm',
        'grid'      : True,
        'title'     : 'Classical Orbital Elements',
        'title_fs'  : 25,
        'wspace'    : 0.3,
        'time_unit' : 'hours',
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