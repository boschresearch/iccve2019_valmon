"""
divergence.py Is called within experiment.py

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
import math
from scipy.stats import entropy


def kullback_leibler_divergence(p, q):
    """
    Computes the Kullback-Leibler divergence for discrete probability
    distribution on same probability space, see
    https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence

    Args:
        p (np.ndarray): discrete probability distribution p
        q (np.ndarray): discrete probability distribution q

    Returns:
        np.ndarray: kld
    """
    p = 1.0 * p / np.sum(p, axis=0)
    q = 1.0 * q / np.sum(q, axis=0)
    # TODO check if eps replacement is good idea to prevent division by zero
    p[p == 0.0] = np.finfo(float).eps
    q[q == 0.0] = np.finfo(float).eps
    kld = np.sum(p * np.log(p / q), axis=0)
    return kld


def kld_two(p, q):
    """
    Kullback-Leibler divergence is not symmetric kld(P|Q) is not kld(Q|P).
    Hence, sum of klds is used to compute distance like measure.
    Args:
        p (np.ndarray): discrete probability distribution p
        q (np.ndarray): discrete probability distribution q

    Returns:
        np.ndarray: kld(P|Q) + kld(Q|P)
    """
    kld_pq = kullback_leibler_divergence(p, q)
    kld_qp = kullback_leibler_divergence(q, p)
    return kld_pq + kld_qp


def jensen_shannon_divergence(p, q):
    # TODO write short doc string
    # https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence

    m = 0.5 * (p+q)
    return 0.5 * entropy(pk=p, qk=m) + 0.5 * entropy(pk=q, qk=m)
