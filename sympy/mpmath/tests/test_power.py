from sympy.mpmath import *
from sympy.mpmath.lib import *

import random

def test_fractional_pow():
    assert mpf(16) ** 2.5 == 1024
    assert mpf(64) ** 0.5 == 8
    assert mpf(64) ** -0.5 == 0.125
    assert mpf(16) ** -2.5 == 0.0009765625
    assert (mpf(10) ** 0.5).ae(3.1622776601683791)
    assert (mpf(10) ** 2.5).ae(316.2277660168379)
    assert (mpf(10) ** -0.5).ae(0.31622776601683794)
    assert (mpf(10) ** -2.5).ae(0.0031622776601683794)
    assert (mpf(10) ** 0.3).ae(1.9952623149688795)
    assert (mpf(10) ** -0.3).ae(0.50118723362727224)

def test_pow_integer_direction():
    """
    Test that inexact integer powers are rounded in the right
    direction.
    """
    random.seed(1234)
    for prec in [10, 53, 200]:
        for i in range(50):
            a = random.randint(1<<(prec-1), 1<<prec)
            b = random.randint(2, 100)
            ab = a**b
            # note: could actually be exact, but that's very unlikely!
            assert to_int(fpow(from_int(a), from_int(b), prec, round_down)) < ab
            assert to_int(fpow(from_int(a), from_int(b), prec, round_up)) > ab


def test_pow_epsilon_rounding():
    """
    Stress test directed rounding for powers with integer exponents.
    Basically, we look at the following cases:

    >>> 1.0001 ** -5
    0.99950014996500702
    >>> 0.9999 ** -5
    1.000500150035007
    >>> (-1.0001) ** -5
    -0.99950014996500702
    >>> (-0.9999) ** -5
    -1.000500150035007

    >>> 1.0001 ** -6
    0.99940020994401269
    >>> 0.9999 ** -6
    1.0006002100560125
    >>> (-1.0001) ** -6
    0.99940020994401269
    >>> (-0.9999) ** -6
    1.0006002100560125

    etc.

    We run the tests with values a very small epsilon away from 1:
    small enough that the result is indistinguishable from 1 when
    rounded to nearest at the output precision. We check that the
    result is not erroneously rounded to 1 in cases where the
    rounding should be done strictly away from 1.
    """

    for (inprec, outprec) in [(100, 20), (5000, 3000)]:

        mp.prec = inprec

        pos10001 = mpf(1) + mpf(2)**(-inprec+5)
        pos09999 = mpf(1) - mpf(2)**(-inprec+5)
        neg10001 = -pos10001
        neg09999 = -pos09999

        mp.prec = outprec
        mp.rounding = 'up'
        assert pos10001**5 > 1
        assert pos09999**5 == 1
        assert neg10001**5 < -1
        assert neg09999**5 == -1
        assert pos10001**6 > 1
        assert pos09999**6 == 1
        assert neg10001**6 > 1
        assert neg09999**6 == 1

        assert pos10001**-5 == 1
        assert pos09999**-5 > 1
        assert neg10001**-5 == -1
        assert neg09999**-5 < -1
        assert pos10001**-6 == 1
        assert pos09999**-6 > 1
        assert neg10001**-6 == 1
        assert neg09999**-6 > 1

        mp.rounding = 'down'
        assert pos10001**5 == 1
        assert pos09999**5 < 1
        assert neg10001**5 == -1
        assert neg09999**5 > -1
        assert pos10001**6 == 1
        assert pos09999**6 < 1
        assert neg10001**6 == 1
        assert neg09999**6 < 1

        assert pos10001**-5 < 1
        assert pos09999**-5 == 1
        assert neg10001**-5 > -1
        assert neg09999**-5 == -1
        assert pos10001**-6 < 1
        assert pos09999**-6 == 1
        assert neg10001**-6 < 1
        assert neg09999**-6 == 1

        mp.rounding = 'ceiling'
        assert pos10001**5 > 1
        assert pos09999**5 == 1
        assert neg10001**5 == -1
        assert neg09999**5 > -1
        assert pos10001**6 > 1
        assert pos09999**6 == 1
        assert neg10001**6 > 1
        assert neg09999**6 == 1

        assert pos10001**-5 == 1
        assert pos09999**-5 > 1
        assert neg10001**-5 > -1
        assert neg09999**-5 == -1
        assert pos10001**-6 == 1
        assert pos09999**-6 > 1
        assert neg10001**-6 == 1
        assert neg09999**-6 > 1

        mp.rounding = 'floor'
        assert pos10001**5 == 1
        assert pos09999**5 < 1
        assert neg10001**5 < -1
        assert neg09999**5 == -1
        assert pos10001**6 == 1
        assert pos09999**6 < 1
        assert neg10001**6 == 1
        assert neg09999**6 < 1

        assert pos10001**-5 < 1
        assert pos09999**-5 == 1
        assert neg10001**-5 == -1
        assert neg09999**-5 < -1
        assert pos10001**-6 < 1
        assert pos09999**-6 == 1
        assert neg10001**-6 < 1
        assert neg09999**-6 == 1

    mp.rounding = 'default'
    mp.dps = 15