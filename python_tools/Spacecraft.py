'''
Spacecraft Class
'''

# Python Standard Libraries


# Third-party Libraries
import numpy             as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# User-defined Libraries
import planetary_data   as pd
import orbit_calcs      as oc
import plotting_tools   as pt

def null_config():
    return {
        'cb'         : pd.earth,
        'coes'       : [],
        'state'      : [],
        'tspan'      : '1',
        'propagator' : 'RK45',
        'atol'       : 1e-6,
        'rtol'       : 1e-6,
        'propagate'  : True
    }

REFERENCE_TIME = '2000-01-01T07:00:00'

class Spacecraft:

    def __init__( self, config ):
        # Assign default configuration
        self.config = null_config()

        # Update configuration parameters with those passed in 
        for key in config.keys():
            self.config[ key ] = config[ key ]
        
        # Central body
        self.cb = self.config[ 'cb' ]

        # Classical orbital elements to state vector
        if self.config[ 'coes' ]:
            self.config[ 'state' ] = oc.sv_from_coe( self.config[ 'coes' ], self.cb[ 'mu' ] )

        # tspan as a str should be the number of orbit periods
        if type( self.config[ 'tspan' ] ) == str:
            self.config[ 'tspan' ] = float( self.config[ 'tspan' ] ) * \
                    oc.period_from_sv( self.config[ 'state' ], self.cb[ 'mu' ] )

        if self.config[ 'propagate' ]:
            self.propagate_orbit()

        self.latlons_calculated = False

    def diffy_q( self, t, states):

        # Unpack states
        x, y, z, vx, vy, vz = states

        # Position vector and its norm
        r     = np.array( [ x, y, z ] ) 
        rnorm = np.linalg.norm( r )

        # Velocity vector
        v = np.array( [vx , vy, vz] )

        # Acceleration vector
        a = - self.cb[ 'mu' ] * r / rnorm**3

        # State vector rates
        states_dot = np.concatenate( (v, a) )

        return states_dot
    

    def propagate_orbit( self ):

        print( 'Propagating orbit...' )

        self.ode_sol = solve_ivp(
            fun    = self.diffy_q,
            t_span = ( 0, self.config[ 'tspan' ]),
            y0     = self.config[ 'state' ],
            method = self.config[ 'propagator' ],
            rtol   = self.config[ 'rtol' ],
            atol   = self.config[ 'atol' ]
        )

        self.states  = self.ode_sol.y.T
        self.times   = self.ode_sol.t
        self.n_steps = self.states.shape[ 0 ]

    def calc_latlons( self ):
        self.latlons = oc.cart2lat( self.states[ :, :3], self.times, REFERENCE_TIME )
        self.latlons_calculated = True

    def plot3( self, label_name, color ):
        pt.plot_3d( self.states[ :, :3], self.cb[ 'radius' ], plt_label = label_name, traj_color = color )

    def plot_groundtrack( self ):
        if not self.latlons_calculated:
            self.calc_latlons()
        
        pt.plot_groundtracks( self.latlons )