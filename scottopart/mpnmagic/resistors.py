# Resistors MPN schema defined here

import re

def rescode_to_value(capcode):
    """TODO: Convert 3-digit resistor value code to resistance in ohms."""
    capcode = capcode.upper()
    if 'R' in capcode:
        # small value
        a = float('{}e-12'.format(capcode.replace('R', '.')))
    else:
        # 2 digits plus exponent
        base = int(capcode[0:2])
        multiplier = int(capcode[2])
        if multiplier == 8: # KEMET uses '8' and '9' for small values
            multiplier = -2
        if multiplier == 9: # KEMET uses '8' and '9' for small values
            multiplier = -1
        a = float('{}e{}'.format(base, multiplier-12))
    return a


# Yageo resistors
res_yageo_re = re.compile(
    '^(?P<manufacturer_series>RC|RE|RT|RL|PT|PA|PE|PS|SR)'
    '(?P<case_package>[0-9]{4})'
    '(?P<resistance_tolerance>[B-W-])'
    '(?P<packaging_code>R|K|C|S)?'
    '(?P<temperature_coefficient>[A-Q-])'
    '(?P<taping_code>[A-Z0-9]{2})'
    '(?P<resistance>[R0-9]{3})'
    '(?P<default_code>L)'
)

def res_yageo_parse(matchgroup):
    lookups = {
        # case_package is already in EIA units
        'capacitance_tolerance' : {
        },
        'dielectric_characteristic' : {
        }
    }
    result = {k:lookups.get(k, {}).get(v, v) for k, v in matchgroup.items()}
    result['manufacturer'] = 'Yageo'
    result['resistance'] = rescode_to_value(matchgroup['resistance'])
    return(result)



res_parsers = [
    (res_yageo_re, res_yageo_parse),
]

def parse_mpn(mpn):
    for regex, fun in res_parsers:
        a = regex.match(mpn)
        if a:
            return fun(a.groupdict())
