"""
plots.py Creates result plots

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


from matplotlib import pyplot as plt
import matplotlib2tikz


def plot_histograms(val_error, val_bin_edges, sim_error):
    plt.figure()
    plt.subplot(121)
    plt.hist(val_error, bins=val_bin_edges, color="blue")
    plt.title("Validation error")

    plt.subplot(122)
    plt.hist(sim_error, bins=val_bin_edges, color="green")
    plt.title("Simulation error")

    matplotlib2tikz.save("Histogram.tex")


def face_validation(time, u, y_model, y_exp, title):

    yaw_rate = y_model[0]
    yaw_rate_experiment = y_exp[0]

    plt.figure()
    ax1 = plt.subplot(211)
    lines = plt.plot(time[::10], u[::10], "k")
    plt.setp(lines, linewidth=2.5)
    plt.ylabel("steer angle in rad")

    plt.subplot(212, sharex=ax1)
    lines = plt.plot(time[::10], yaw_rate[::10], "r",
                     time[::10], yaw_rate_experiment[::10], ":k")
    plt.setp(lines, linewidth=2.5)
    plt.legend(["single track model", "CarMaker"], loc=3)
    plt.xlabel("time in seconds")
    plt.ylabel("yaw rate in rad per seconds")

    matplotlib2tikz.save(title + ".tex")


def plot_monitor(idx, divergence, title):
    plt.figure()
    plt.plot(idx[::10], divergence[::10], "k")
    plt.xlabel("time in seconds")
    plt.ylabel("Jensen-Shannon divergence")

    matplotlib2tikz.save(title + ".tex")
