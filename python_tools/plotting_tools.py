'''
Plotting tools
'''

import os
import csv
import numpy                as     np 
import matplotlib.pyplot    as     plt
from   mpl_toolkits.mplot3d import Axes3D
from   matplotlib.image     import imread
from   PIL                  import Image
from   matplotlib           import cm


plt.style.use( 'dark_background' )

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
    latitudes = []
    longitudes = []

    # Read the csv file
    with open( EARTH_COASTLINES, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            longitude, latitude = map(float, row)
            longitudes.append(longitude)
            latitudes.append(latitude)

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
            ax.plot(segment_lon, np.array(segment_lat), 'b')  # Use a fixed color 'b' (blue)
            # Start a new segment
            segment_lat = [lat]
            segment_lon = [lon]
        else:
            # Continue the current segment
            segment_lat.append(lat)
            segment_lon.append(lon)
        prev_lon = lon

    # Plot the last segment
    ax.plot(segment_lon, np.array(segment_lat), 'b')  # Use a fixed color 'b' (blue)

    # Mark start and end points
    ax.scatter(coords[0, 0], -coords[0, 1], color='g', s=100, label='Start')
    ax.scatter(coords[-1, 0], -coords[-1, 1], color='r', s=100, label='End')

    # Plot coastlines
    ax.scatter(longitudes, latitudes, s=0.1, color='m')

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