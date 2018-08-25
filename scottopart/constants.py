import math

e3 = (1.0, 2.2, 4.7)
e6 = (1.0, 1.5, 2.2, 3.3, 4.7, 6.8)
e12 = (1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2)
e24 = (1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
       3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1)


def split_valuestring(input):
    # Don't forget to handle '\u03a9'(capital omega) and '\u2126' (ohm sign)
    # And '\u03bc' (greek mu) and '\u00b5' (micro sign)
    a = EngineerIO.EngineerIO(units=frozenset(['A', 'Ω', 'Ω', 'F', 'H', 'V', 'W']),
                              suffices=[["y"], ["z"], ["a"], ["f"], ["p"], ["n"], ["\u00b5", "\u03bc", "u"], ["m"], [], ["k"], ["M"], ["G"], ["T"], ["E"], ["Z"], ["Y"]])
    # Return val, unit
    return a.safe_normalize(input)


def format_value(v, unit='', with_space=True):
    """
    Format v using SI suffices with optional units.
    Suppress trailing zeros.
    """
    exp_suffix_map = {
        -5: 'f',
        -4: 'p',
        -3: 'n',
        -2: 'u',
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
    return "{0} {1}".format(res, suffix) if suffix else res
