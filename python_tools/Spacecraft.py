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
        'cb'          : pd.earth,
        'coes'        : [],
        'state'       : [],
        'tspan'       : '1',
        'propagator'  : 'RK45',
        'atol'        : 1e-6,
        'rtol'        : 1e-6,
        'propagate'   : True,
        'orbit_perts' : {}
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

        # Set initial status for calculations
        self.latlons_calculated = False
        self.coes_calculated    = False

        # Set initial states
        self.state0       = np.zeros( 6 )
        self.state0[ :6 ] = self.config[ 'state' ]

        # Assign orbit perturbation functions
        self.orbit_perts = self.config[ 'orbit_perts' ]
        self.assign_orbit_perturbations_functions()

        # Propagates the orbit
        if self.config[ 'propagate' ]:
            self.propagate_orbit()

    def diffy_q( self, t, states):

        # Unpack states
        x, y, z, vx, vy, vz = states

        states_dot = np.zeros( 6 )

        # Position vector and its norm
        r     = np.array( [ x, y, z ] ) 
        rnorm = np.linalg.norm( r )

        # Velocity vector
        v = np.array( [vx , vy, vz] )

        # Acceleration vector
        a = - self.cb[ 'mu' ] * r / rnorm**3

        # Include perturbations, if any
        for pert in self.orbit_perts_funcs:
            a += pert( states )

        # State vector rates
        states_dot[ :3 ]  = v
        states_dot[ 3:6 ] = a

        return states_dot
    
    def assign_orbit_perturbations_functions( self ):

        self.orbit_perts_funcs_map = {
            'J2'    : self.calc_J2,
            'SRP'   : self.calc_SRP,
            'ATM'   : self.calc_atm_drag,
            '3body' : self.calc_third_body_perts
        }

        self.orbit_perts_funcs = []

        for key, value in self.config[ 'orbit_perts' ].items():
            if value: # Only add the function if the perturbation is set to True
                self.orbit_perts_funcs.append(
                    self.orbit_perts_funcs_map[ key ]
                )

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
    
    def calc_coes ( self ):
        self.coes = np.zeros( ( self.n_steps, 6 ) )

        for n in range( self.n_steps ):
            self.coes[ n, : ] = oc.coe_from_sv(
                self.states[ n, : ],
                args = {
                    'mu'  : self.cb[ 'mu' ],
                    'deg' : True
                } 
            )
        
        self.coes_rel        = self.coes[ : ] - self.coes[ 0, : ]
        self.coes_calculated = True

    def calc_latlons( self ):
        self.latlons            = oc.cart2lat( self.states[ :, :3], self.times, REFERENCE_TIME )
        self.latlons_calculated = True
    
    def calc_J2( self, state ):
        '''
        Returns the perturbing gravitational acceleration vector (p) due to J2
        '''
        x, y, z = state[ :3 ] 
        r       = np.linalg.norm( state[ :3 ] )
        p       = np.zeros( 3 )

        tx = x / r * ( 5 * z**2 / r**2 - 1 )
        ty = y / r * ( 5 * z**2 / r**2 - 1 )
        tz = z / r * ( 5 * z**2 / r**2 - 3 )

        p = 3 / 2 * self.cb[ 'J2' ] * self.cb[ 'mu' ] * self.cb[ 'radius' ]**2 / r**4 * np.array( [ tx, ty, tz ] )

        return p

    def calc_SRP( self, state ):
        pass

    def calc_atm_drag( self, state ):
        pass

    def calc_third_body_perts( self ):
        pass

    def plot_coes( self, args = { 'show' : True }, step = 1 ):
        if not self.coes_calculated:
            self.calc_coes()

        pt.plot_coes( self.times[ ::step ], [ self.coes[ ::step ] ], args )

    def plot_3d( self, args = {} ):
        pt.plot_3d( [ self.states[ :, :3] ], 
            args = {
                'show'      : True,
                'cb_radius' : self.cb[ 'radius' ],
                'traj_lws'  : 1 
            }
        )

    def plot_states( self, args = { 'show' : True} ):
        pt.plot_states( self.times, self.states, args )

    def plot_positions( self, args = { 'show' : True, 'time_unit' : 'hours' } ):
        pt.plot_pos( self.times, self.states[ :, :3 ], args )

    def plot_velocities( self, args = { 'show' : True, 'time_unit' : 'hours' } ):
        pt.plot_velocities( self.times, self.states[ :, 3: ], args )

    def plot_groundtrack( self ):
        if not self.latlons_calculated:
            self.calc_latlons()
        
        pt.plot_groundtracks( self.latlons )