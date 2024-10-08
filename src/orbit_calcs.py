'''
Trajectory Calculation Tools
'''

# Python Standard Libraries


# Third-party Libraries
from astropy.time import Time
import numpy as np

# Orbital-Mechanics Libraries
import numerical_tools as nt
from numerical_tools import norm
import planetary_data as pd

r2d = 180 / np.pi
d2r = 1 / r2d
sec2day = 1 / 3600 / 24


def sv_from_coe( coe, mu, deg = True ):
    '''
    Returns state vector from the classical orbital elements
    '''
    # get states
    sma, ecc, incl, raan, aop, ta = coe

    if deg == True:
        incl *= np.pi/180
        raan *= np.pi/180
        aop  *= np.pi/180
        ta   *= np.pi/180

    # determine position and velocity vector in perifocal frame
    r_p = sma * ( 1 - ecc**2) / ( 1 + ecc * np.cos(ta) ) *\
            np.array( [ np.cos( ta ), np.sin( ta ), 0 ] )
    
    v_p = np.sqrt( mu / ( sma * ( 1 - ecc**2 ) ) ) *\
            np.array( [ -np.sin( ta ), ecc + np.cos( ta ), 0 ] )

    # Find rotation (DCM) matrix from ECI to perifocal frame
    R_pI = nt.R3( aop ) @ nt.R1( incl ) @ nt.R3( raan )

    # Perform coordinate transformation
    r_I = R_pI.T @ r_p
    v_I = R_pI.T @ v_p

    # concatenate arrays
    sv = np.concatenate( (r_I, v_I) )

    return sv

def coe_from_sv( state, args = {} ):
    '''
    Returns the classical orbital elements when provided the state vector 
    '''
    _args = {
        'mu'         : pd.earth[ 'mu' ],
        'deg'        : True,
        'print_coes' : False
    }

    for key in args.keys():
        _args[ key ] = args[ key ]


    small = 1e-12

    r      = state[ :3 ]
    v      = state[ 3:6 ]
    norm_r = norm( r )
    norm_v = norm( v )

    h      = np.cross( r, v )
    norm_h = norm( h )

    if norm_h >= small:
        n      = np.array( [ -h[ 1 ], h[ 0 ], 0.0 ] )
        norm_n = norm( n )
        c1     = norm_v**2 - _args[ 'mu' ] / norm_r
        rdotv  = np.dot( r, v )
        e      = ( c1 * r - rdotv * v ) / _args[ 'mu' ]
        norm_e = norm(e)

        sme = ( norm_v**2 * 0.5 ) - ( _args[ 'mu' ] / norm_r )
        if abs(sme) > small:
            a = -_args[ 'mu' ] / ( 2.0 * sme )
        else:
            a = np.inf

        p = norm_h**2 / _args[ 'mu' ]

        hk = h[2] / norm_h
        incl = np.arccos(hk)

        if norm_n > small:
            temp = n[0] / norm_n
            temp = np.clip(temp, -1.0, 1.0)
            raan = np.arccos(temp)
            if n[1] < 0.0:
                raan = 2 * np.pi - raan
        else:
            raan = 0

        if norm_e > small:
            temp = np.dot(n, e) / (norm_n * norm_e)
            temp = np.clip(temp, -1.0, 1.0)
            aop  = np.arccos(temp)
            if e[2] < 0.0:
                aop = 2 * np.pi - aop
        else:
            aop = 0

        if norm_e > small:
            temp = np.dot(e, r) / (norm_e * norm_r)
            temp = np.clip(temp, -1.0, 1.0)
            ta   = np.arccos(temp)
            if rdotv < 0.0:
                ta = 2 * np.pi - ta
        else:
            ta = 0

        #------ Include special cases later

        # Radians to degrees
        if _args[ 'deg' ] == True:
            incl    *= r2d
            raan *= r2d
            aop  *= r2d
            ta   *= r2d
        
        # Print coes
        if _args[ 'print_coes' ]:
            print( 'a'   , a    )
            print( 'e'   , norm_e    )
            print( 'i'   , incl    )
            print( 'RAAN', raan )
            print( 'AOP' , aop  )
            print( 'TA'  , ta   )
            print()


    else:
        a = norm_e = incl = raan = aop = ta = None

    return [ a, norm_e, incl, raan, aop, ta ] 

def period_from_sv( state, mu ):
    '''
    Returns orbital period (sec) when given the state vector

    Note: not valid for open orbits (parabolic, hyperbolic)
    '''
    # get position and velocity vector
    r = state[  :3 ]
    v = state[ 3:6 ]

    # get norm r and v
    rnorm = norm( r )
    vnorm = norm( v )

    # vis-visa eq.
    e = vnorm**2 / 2 - mu / rnorm

    # semi-major axis
    a = - mu / (2 * e)

    return 2 * np.pi * ( a** 3 / mu ) ** ( 0.5 )

def cart2lat( r_ECI, times, reference_time = '2000-01-01T00:00:00' ):
    '''
    Converts Cartesian coordinates in ECI frame to lat and long coordinates
    in the ECEF frame.
    
    Parameters:
    - r_ECI: Array of Cartesian coordinates in the ECI frame (shape: [steps, 3]).
    - times: Array of times corresponding to the Cartesian coordinates (shape: [steps]).

    Returns:
    - latlons: Array of latitude and longitude coordinates in the ECEF frame (shape: [steps, 2]).
    '''
    steps   = r_ECI.shape[ 0 ]
    latlons = np.zeros( (steps, 2) )

    # Ensure the reference time is a valid ISO format string
    reference_time = reference_time.strip()

    # Convert reference time to astropy Time object
    t_ref = Time( reference_time, format = 'isot', scale='utc' )

    # Compute the initial GST
    initial_gst = t_ref.sidereal_time( 'mean', 'greenwich' ).deg

    # Earth's rotation rate in degrees per second (approximately 360 deg/86400 sec)
    omega_earth = 360 / 86164.0905 # Use the sidereal day for more accuracy

    for step in range( steps ):
        # Compute the rotation angle based on Earth's rotation rate
        theta = omega_earth * times[ step ]
        theta = theta % 360 # ensure the angle is within [0,360] deg

        # Get rotation matrix (rotation about the z-axis)
        R = nt.R3( theta * d2r )

        # Perform coordinate transformation 
        r_ECEF = R @ r_ECI[ step ]

        # Calculate latitude and longitude coords in ECEF frame
        latlons[ step ] =  ra_and_dec_from_r( r_ECEF, deg = True )

        # Ensure the longitude is within -180 to 180 degrees
        latlons[ step, 0 ] = ( ( latlons[ step, 0 ] + 180 ) % 360 ) - 180

    return latlons


def ra_and_dec_from_r( state, deg = True ):
    '''
    Return the right ascension and declination from the position vector of a satellite
    '''
    # Extract coodinates
    X = state[ 0 ]
    Y = state[ 1 ]
    Z = state[ 2 ]

    # Calculate magnitude of position vector
    r = np.sqrt( X**2 + Y**2 + Z**2 )

    # Calculate the direction cosines of r
    l, m, n = X/r, Y/r, Z/r

    # Calculate the declination
    dec = np.arcsin( n )

    # Calculate the right ascension
    if m > 0:
        ra = np.arccos( l / np.cos( dec ) )
    elif m < 0:
        ra = 2 * np.pi - np.arccos( l / np.cos( dec ) )
    else:
        ra = np.nan
        print("Quadrant ambiguity could not be resolved for right ascension")

    if deg:
        ra  *= r2d
        dec *= r2d  
    
    return ra, dec

def get_gst():
    '''
    Calculate Greenwhich Sidereal Time (GST) using astropy.
    '''
    # Get the current time in UTC
    t = Time.now()

    # Calculate the Greenwhich Sidereal Time
    gst = t.sidereal_time( 'mean', 'greenwich')

    return gst


if __name__ == '__main__':
    state = np.array ( [ -6045, -3490, 2500, -3.457, 6.618, 2.533 ] )
    a, e, i, raan, aop, ta = coe_from_sv(
        state, 
        args = {
            'print_coes' : True
        }
    )