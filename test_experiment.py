"""
test_experiment.py Pytest file

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
from numpy.testing.utils import assert_allclose

from divergence import kullback_leibler_divergence, kld_two
from scipy.stats import entropy

absolute_tolerance = 1e-7


def test_kld_pq():
    # see example here:
    # https://fr.wikipedia.org/wiki/Divergence_de_Kullback-Leibler
    p = np.array([0.36, 0.48, 0.16])
    q = np.array([0.333, 0.333, 0.333])
    correct_value = entropy(pk=p, qk=q)

    test_value = kullback_leibler_divergence(p=p, q=q)
    assert_allclose(test_value, correct_value, atol=absolute_tolerance,
                    verbose=True)


def test_kld_qp():
    # see example here:
    # https://fr.wikipedia.org/wiki/Divergence_de_Kullback-Leibler
    p = np.array([0.36, 0.48, 0.16])
    q = np.array([0.333, 0.333, 0.333])
    correct_value = entropy(pk=q, qk=p)

    test_value = kullback_leibler_divergence(p=q, q=p)
    assert_allclose(test_value, correct_value, atol=absolute_tolerance,
                    verbose=True)


def test_kld_two():
    p = np.array([0.36, 0.48, 0.16])
    q = np.array([0.333, 0.333, 0.333])
    correct_value = entropy(pk=p, qk=q) + entropy(pk=q, qk=p)

    test_value = kld_two(p, q)
    assert_allclose(test_value, correct_value, atol=absolute_tolerance,
                    verbose=True)
