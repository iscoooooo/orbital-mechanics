'''
Trajectory Calculation Tools
'''

# Python Standard Libraries


# Third-party Libraries
import numpy           as np

# Orbital-Mechanics Libraries
import numerical_tools as nt


def sv_from_coe( coe, mu ):
    '''
    Returns state vector from the classical orbital elements
    '''
    # get states
    sma, ecc, incl, raan, omega, ta = coe

    # determine position and velocity vector in perifocal frame
    r_p = sma * ( 1 - ecc**2) / ( 1 + ecc * np.cos(ta) ) *\
            np.array( [ np.cos( ta ), np.sin( ta ), 0 ] )
    
    v_p = np.sqrt( mu / ( sma * ( 1 - ecc**2 ) ) ) *\
            np.array( [ -np.sin( ta ), ecc + np.cos( ta ), 0 ] )

    # Find rotation (DCM) matrix from ECI to perifocal frame
    R_pI = nt.R3( omega ) @ nt.R1( incl ) @ nt.R3( raan )

    # Perform coordinate transformation
    r_I = R_pI.T @ r_p
    v_I = R_pI.T @ v_p

    # concatenate arrays
    sv = np.concatenate( (r_I, v_I) )

    return sv

def period_from_sv( state, mu ):
    '''
    Returns orbital period (sec) when given the state vector

    Note: not valid for open orbits (parabolic, hyperbolic)
    '''
    # get position and velocity vector
    r = state[  :3 ]
    v = state[ 3:6 ]

    # get norm r and v
    rnorm = np.linalg.norm( r )
    vnorm = np.linalg.norm( v )

    # vis-visa eq.
    e = vnorm**2 / 2 - mu / rnorm

    # semi-major axis
    a = - mu / (2 * e)

    return 2 * np.pi * ( a** 3 / mu ) ** ( 0.5 )