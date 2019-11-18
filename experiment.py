"""
experiment.py Run this file to reproduce results of the paper

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

import numpy as np
import matplotlib.pyplot as plt

from divergence import jensen_shannon_divergence
from models import simulate_single_track_model
from plots import plot_histograms, face_validation, plot_monitor
from scipy.optimize import minimize


class CircularBuffer:
    def __init__(self, length):
        self.length = length
        self.buffer = np.full(shape=length, fill_value=None)

    def update(self, value):
        self.buffer = np.append(self.buffer[1::], value)

    def is_filled(self):
        return (self.get() !=
                np.full(shape=self.length, fill_value=None)).all()

    def get(self):
        return self.buffer


def read_carmaker_data(file):
    """
    Args:
        file: csv file from carmaker

    Returns:
        t: time vector
        u: steer angle for vehicle single track model
        y_exp: yaw rate from carmaker

    """
    dat = np.genfromtxt(file, delimiter=",", comments="#", names=True)
    t = dat["Time"]
    u = dat["DriverSteerAng"]
    y_exp = np.vstack((dat["CarYawRate"],
                       dat["CarSideSlipAngle"]))

    return t, u, y_exp


def objective_func(x):
    yout, xout = simulate_single_track_model(c_f=x[0], c_r=x[1], l_f=l_f,
                                             l_r=l_r, m=m, theta=theta,
                                             v=velocity, ratio=ratio,
                                             t=time, u=steer_angle,
                                             x0=np.matrix([[0], [0]]))

    err0 = y_experiment[0] - yout[0]
    err1 = y_experiment[1] - yout[1]

    scaled_err0 = (err0 - np.min(err0)) / (np.max(err0) - np.min(err0))
    scaled_err1 = (err1 - np.min(err1)) / (np.max(err1) - np.min(err1))

    objective = np.sum(scaled_err0 ** 2) + np.sum(scaled_err1 ** 2)
    return objective


def parameter_fitting():
    x0 = np.array([60000, 60000])
    res = minimize(fun=objective_func, x0=x0,
                   method='Powell', options={'disp': True})
    print("Optimized params")
    print(res.x)
    return res.x


# Parameter estimation #########################################################
time, steer_angle, y_experiment = read_carmaker_data(
    file="slalom1_14_5ms.CSV")
velocity = 14.5

l_f = 0.968
l_r = 1.582
m = 1856.2
theta = 2806.23
ratio = 20

optimized_params = parameter_fitting()
c_f = optimized_params[0]
c_r = optimized_params[1]

yout, xout = simulate_single_track_model(c_f=c_f, c_r=c_r, l_f=l_f, l_r=l_r,
                                         m=m, theta=theta, v=velocity,
                                         ratio=ratio, t=time, u=steer_angle,
                                         x0=np.matrix([[0], [0]]))

face_validation(time=time, u=steer_angle, y_model=yout,
                y_exp=y_experiment, title="Parameter estimation")

# Validation ###################################################################
time, steer_angle, y_experiment = read_carmaker_data(
    file="experiment2_40kmh.CSV")

noise_scale = 0.001
noise_loc = 0.0
noise = np.random.normal(loc=noise_loc, scale=noise_scale,
                         size=(y_experiment.shape))
y_experiment = y_experiment + noise

velocity = 40 / 3.6

yout, xout = simulate_single_track_model(c_f=c_f, c_r=c_r, l_f=l_f, l_r=l_r,
                                         m=m, theta=theta, v=velocity,
                                         ratio=ratio, t=time, u=steer_angle,
                                         x0=np.matrix([[0], [0]]))

face_validation(time=time, u=steer_angle, y_model=yout,
                y_exp=y_experiment, title="Validation")

val_error = y_experiment[0] - yout[0]
val_hist, val_bin_edges = np.histogram(val_error, bins=20)

# Simulate model outside validation space ######################################
time, steer_angle, y_experiment = read_carmaker_data(
    file="experiment3_40kmh.CSV")

noise=np.random.logistic(loc=0.001,scale=noise_scale*1.5,size=(
    y_experiment.shape))

y_experiment = y_experiment + noise

velocity = 40 / 3.6

yout, xout = simulate_single_track_model(c_f=c_f, c_r=c_r, l_f=l_f, l_r=l_r,
                                         m=m, theta=theta, v=velocity,
                                         ratio=ratio, t=time, u=steer_angle,
                                         x0=np.matrix([[0], [0]]))

face_validation(time=time, u=steer_angle, y_model=yout,
                y_exp=y_experiment, title="Simulation")

simulation_error = y_experiment[0] - yout[0]
simulation_hist = np.histogram(simulation_error, bins=val_bin_edges)[0]

# Histogram and kld_two for all data
plot_histograms(val_error=val_error,
                val_bin_edges=val_bin_edges,
                sim_error=simulation_error)

# Online validity monitor#######################################################
idx = np.arange(0, time.shape[0], 1)
jsd = np.full(time.shape[0], np.nan)
buffer = CircularBuffer(length=300)

for i in idx:
    buffer.update(simulation_error[i])
    if buffer.is_filled():
        online_sim_hist = np.histogram(buffer.get(), bins=val_bin_edges)[0]
        jsd[i] = jensen_shannon_divergence(p=val_hist, q=online_sim_hist)


plot_monitor(time, jsd, "JSD")

plt.show()
