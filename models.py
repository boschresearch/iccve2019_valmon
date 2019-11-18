"""
models.py Contains the single track model and is called in experiment.py

Copyright (c) 2019 Robert Bosch GmbH

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""


import control
import numpy as np


def simulate_single_track_model(c_f, c_r, l_f, l_r, m, theta, v, ratio, t, u,
                                x0):
    """
    Vehicle single track model from [p. 230, Schramm2018]
    states = [\dot{psi} in rad/s\\
              beta in rad]
    Args:
        c_f: Front cornering stiffness [N/rad]
        c_r: Rear cornering stiffness [N/rad]
        l_f: Distance CoG to front axles [m]
        l_r: Distance CoG to rear axles [m]
        m: Vehicle mass [kg]
        theta: Vehicle yaw inertia [kgm^2]
        v: Vehicle Speed [m/s]
        ratio: Steerangle ratio [-]
        t: simulation time vector
        u: input vector
        x0: initial state

    Returns:
        y: output vector
        x: sates
    """
    a_11 = -1 / v * (c_f * l_f ** 2 + c_r * l_r ** 2) / theta
    a_12 = -(c_f * l_f - c_r * l_r) / theta
    a_21 = -1 - 1 / (v ** 2) * (c_f * l_f - c_r * l_r) / m
    a_22 = -1 / v * (c_f + c_r) / m
    a_matrix = np.matrix([[a_11, a_12], [a_21, a_22]])

    b_1 = (c_f * l_f) / theta
    b_2 = 1 / v * c_f / m
    b_matrix = np.matrix([[b_1], [b_2]])

    c_matrix = np.matrix([[1, 0], [0, 1]])
    d_matrix = np.matrix([[0], [0]])

    ss_model = control.ss(a_matrix, b_matrix, c_matrix, d_matrix)

    y, x = control.forced_response(ss_model, T=t, U=u/ratio, X0=x0)[1:3]
    return y, x
