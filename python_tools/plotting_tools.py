'''
Plotting tools
'''

import os
import numpy                as     np 
import matplotlib.pyplot    as     plt
from   mpl_toolkits.mplot3d import Axes3D
from   matplotlib.image     import imread
from   PIL                  import Image
from   matplotlib           import cm


plt.style.use( 'dark_background' )


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