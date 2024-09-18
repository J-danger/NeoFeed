import numpy as np
import plotly.graph_objects as go
from skyfield.constants import AU_KM
from skyfield.api import load
from scipy.constants import G
from math import pi, sqrt, cos, sin
from flask import Flask, jsonify
from utils.satellite_positions import fetch_and_convert_tle_data
import json

# Constants
mu_sun = 1.32712440018e11  # Gravitational parameter of the Sun in km^3/s^2

from skyfield.api import load

def get_planet_positions():
    # Load the planetary ephemeris data
    ts = load.timescale()
    planets = load('de421.bsp')  # Load DE421 ephemeris data

    # Define the timescale and current time
    t = ts.now()

    # Get the planets
    earth, venus, mars = planets['earth'], planets['venus'], planets['mars']

    # Get current positions
    earth_pos = earth.at(t).position.au  # Position in astronomical units
    venus_pos = venus.at(t).position.au
    mars_pos = mars.at(t).position.au

    # Convert AU to km
    positions = {
        'Sun': [0, 0, 0],
        'Earth': [earth_pos[0] * AU_KM, earth_pos[1] * AU_KM, earth_pos[2] * AU_KM],
        'Venus': [venus_pos[0] * AU_KM, venus_pos[1] * AU_KM, venus_pos[2] * AU_KM],
        'Mars': [mars_pos[0] * AU_KM, mars_pos[1] * AU_KM, mars_pos[2] * AU_KM],
    }
    return positions


def plot_orbit(orbital_data_list, orbiting_body):
    # print('body in image function', orbiting_body)
    fig = go.Figure()
    # print(orbiting_body)
    orbiting_planet = max(set(orbiting_body), key=orbiting_body.count)    
    # Get positions for the Sun and other planets
    planet_positions = get_planet_positions()
    satellite_positions = fetch_and_convert_tle_data()
    parsed_dict = json.loads(satellite_positions)
    print(parsed_dict)
    # for satellite in satellite_positions:
    #     print(satellite)
    for orbital_data in orbital_data_list:
        # Extract orbital parameters from the data
        a = float(orbital_data['semi_major_axis']) * AU_KM  # Semi-major axis in km
        # if central_body == 'sun':
        #     a = float(orbital_data['semi_major_axis']) * AU_KM  # Semi-major axis in km
        e = float(orbital_data['eccentricity'])  # Eccentricity
        i = float(orbital_data['inclination']) * (pi / 180)  # Inclination in radians
        omega = float(orbital_data['ascending_node_longitude']) * (pi / 180)  # Longitude of ascending node in radians
        w = float(orbital_data['perihelion_argument']) * (pi / 180)  # Argument of perihelion in radians
        M0 = float(orbital_data['mean_anomaly']) * (pi / 180)  # Mean anomaly at epoch in radians
        period = float(orbital_data['orbital_period']) * 86400  # Orbital period in seconds

        # Generate time values over one orbit period
        num_points = 500
        time = np.linspace(0, period, num_points)

        # Calculate mean motion
        n = sqrt(mu_sun / a**3)  # Mean motion (radians per second)

        # Calculate position over time
        r_x, r_y, r_z = [], [], []
        for t in time:
            # Mean anomaly
            M = M0 + n * t
            # Solve Kepler's equation for Eccentric Anomaly using Newton's method
            E = M
            for _ in range(10):
                E = E - (E - e * sin(E) - M) / (1 - e * cos(E))
            # True anomaly
            nu = 2 * np.arctan2(sqrt(1 + e) * sin(E / 2), sqrt(1 - e) * cos(E / 2))
            # Distance from focus (Sun) to object
            r = a * (1 - e * cos(E))
            # Position in orbital plane
            x_orb = r * cos(nu)
            y_orb = r * sin(nu)

            # Rotate to celestial coordinates
            x = (cos(omega) * cos(w + nu) - sin(omega) * sin(w + nu) * cos(i)) * r
            y = (sin(omega) * cos(w + nu) + cos(omega) * sin(w + nu) * cos(i)) * r
            z = (sin(i) * sin(w + nu)) * r

            r_x.append(x)
            r_y.append(y)
            r_z.append(z)

        # Add each orbit path to the plot
        fig.add_trace(go.Scatter3d(
            x=r_x, y=r_y, z=r_z,
            mode='lines',
            name=f'Orbit Path {orbital_data["orbit_id"]}'
        ))

    # Plot positions of the Sun and planets
    for body, pos in planet_positions.items():
        fig.add_trace(go.Scatter3d(
            x=[pos[0]], y=[pos[1]], z=[pos[2]],
            mode='markers',
            marker=dict(size=8 if body == 'Sun' else 5, color='red' if body == 'Sun' else 'orange'),
            name=body
        ))

    # Set labels and title
    fig.update_layout(
        scene=dict(
            xaxis_title='X (km)',
            yaxis_title='Y (km)',
            zaxis_title='Z (km)',
            aspectmode='data'  # Keeps the aspect ratio consistent
        ),
    )

    # Convert the figure to JSON
    fig_json = fig.to_dict()

    return fig_json
