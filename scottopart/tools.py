# Utilities

import math

def split_valuestring(input):
    # Don't forget to handle '\u03a9'(capital omega) and '\u2126' (ohm sign)
    # And '\u03bc' (greek mu) and '\u00b5' (micro sign)
    a = EngineerIO.EngineerIO(units=frozenset(['A', 'Ω', 'Ω', 'F', 'H', 'V', 'W']),
                              suffices=[["y"], ["z"], ["a"], ["f"], ["p"], ["n"], ["\u00b5", "\u03bc", "u"], ["m"], [], ["k"], ["M"], ["G"], ["T"], ["E"], ["Z"], ["Y"]])
    # Return val, unit
    return a.safe_normalize(input)


def format_value(v, unit='', with_space=True, with_unicode=False):
    """
    Format v using SI suffices with optional units.
    Suppress trailing zeros.
    """
    exp_suffix_map = {
        -5: 'f',
        -4: 'p',
        -3: 'n',
        -2: '\u00b5' if with_unicode else 'u',
        -1: 'm',
        0: '',
        1: 'k',
        2: 'M',
        3: 'G',
    }
    # Suffix map is indexed by one third of the decadic logarithm.
    exp = 0 if v == 0. else math.log(abs(v), 10.)
    suffixMapIdx = int(math.floor(exp / 3.))
    # Ensure we're in range
    if not min(exp_suffix_map.keys()) < suffixMapIdx < max(
            exp_suffix_map.keys()):
        raise ValueError("Value out of range: {0}".format(v))
    # Pre-multiply the value
    v = v * (10.0 ** -(suffixMapIdx * 3))

    res = '{:.5g}'.format(v)
    suffix = exp_suffix_map[suffixMapIdx] + unit
    sep = ' ' if with_space else ''
    return '{0}{1}{2}'.format(res, sep, suffix) if suffix else res
