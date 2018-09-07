# Capacitors MPN schema defined here

import re

def capcode_to_value(capcode):
    """Convert 3-digit capacitor value code to capacitance in F."""
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


# Murata ceramic capacitors (beware: GCM is automotive)
cap_murata_re = re.compile(
    '^(?P<manufacturer_series>GRM|GJM|GCM|GCJ)'
    '(?P<case_package>[0-9DU]{2})'
    '(?P<size_thickness>[2-9A-Z]{1})'
    '(?P<dielectric_characteristic>[0-9A-Z]{2})'
    '(?P<voltage_rating_dc>[0-9A-Z]{2})'
    '(?P<capacitance>[R0-9]{3})'
    '(?P<capacitance_tolerance>[A-Z])'
    '(?P<spec_code>[A-Z0-9]{3})?'
    '(?P<packaging_code>[A-Z])?'
)


def cap_murata_parse(matchgroup):
    lookups = {
        'case_package' : {
            '03' : '0201',
            '15' : '0402',
            '18' : '0603',
            '21' : '0805',
            '31' : '1206',
            '32' : '1210',
            '43' : '1812',
            '55' : '2220'
        },
        'size_thickness' : {
            '2' : '0.2 mm',
            '3' : '0.3 mm',
            '4' : '0.4 mm',
            '5' : '0.5 mm',
            '6' : '0.6 mm',
            '7' : '0.7 mm',
            '8' : '0.8 mm',
            '9' : '0.85 mm',
            'A' : '1.0 mm',
            'B' : '1.25 mm',
            'C' : '1.6 mm',
            'D' : '2.0 mm',
            'E' : '2.5 mm',
            'M' : '1.15 mm',
            'Q' : '1.5 mm'
        },
        'dielectric_characteristic' : {
            '5C' : 'C0G/NP0',
            '7U' : 'U2J',
            'C7' : 'X7S',
            'C8' : 'X6S',
            'D7' : 'X7T',
            'D8' : 'X6T',
            'E7' : 'X7U',
            'R6' : 'X5R',
            'R7' : 'X7R',
            'W0' : 'X7T',
            'R9' : 'X8R'
        },
        'voltage_rating_dc' : {
            '0E' : 2.5,
            '0G' : 4,
            '0J' : 6.3,
            '1A' : 10,
            '1C' : 16,
            '1E' : 25,
            'YA' : 35,
            '1H' : 50,
            '1J' : 63,
            '1K' : 80,
            '2A' : 100,
            '2D' : 200,
            '2E' : 250,
            '2W' : 450,
            '2H' : 500,
            '2J' : 630,
            '3A' : 1000,
            '3D' : 2000
        },
        'capacitance_tolerance' : {
            'B' : '±0.1pF',
            'C' : '±0.25pF',
            'D' : '±0.5%',
            'F' : '1%',
            'G' : '2%',
            'J' : '5%',
            'K' : '10%',
            'M' : '20%',
            'W' : '±0.05pF'
        }
    }
    result = {k:lookups.get(k, {}).get(v, v) for k, v in matchgroup.items()}
    result['manufacturer'] = 'Murata'
    result['capacitance'] = capcode_to_value(matchgroup['capacitance'])
    if result['manufacturer_series'] in ['GCJ']:
        result['is_automotive'] = True
    return(result)

# Samsung ceramic capacitors
cap_samsung_re = re.compile(
    '^(?P<manufacturer_series>CL)'
    '(?P<case_package>[0-5]{2})'
    '(?P<dielectric_characteristic>[A-Z])'
    '(?P<capacitance>[R0-9]{3})'
    '(?P<capacitance_tolerance>[A-Z])'
    '(?P<voltage_rating_dc>[A-Z])'
    '(?P<size_thickness>[0-9A-Z])'
    '(?P<plating_code>[A-Z])?'
    '(?P<control_code>[A-Z])?'
    'N'
    '(?P<packaging_code>[A-Z])?'
)

def cap_samsung_parse(matchgroup):
    lookups = {
        'case_package' : {
            '03' : '0201',
            '05' : '0402',
            '10' : '0603',
            '21' : '0805',
            '31' : '1206',
            '32' : '1210',
            '43' : '1812',
            '55' : '2220'
        },
        'dielectric_characteristic' : {
            'C' : 'C0G/NP0',
            'U' : 'U2J',
            'A' : 'X5R',
            'B' : 'X7R',
            'X' : 'X6S',
            'F' : 'Y5V'
        },
        'capacitance_tolerance' : {
            'A' : '±0.05pF',
            'B' : '±0.1pF',
            'C' : '±0.25pF',
            'D' : '±0.5%',
            'F' : '1%',
            'G' : '2%',
            'J' : '5%',
            'K' : '10%',
            'M' : '20%',
            'Z' : '+80/-20%'
        },
        'voltage_rating_dc' : {
            'R' : 4,
            'Q' : 6.3,
            'P' : 10,
            'O' : 16,
            'A' : 25,
            'L' : 35,
            'B' : 50,
            'C' : 100,
            'D' : 200,
            'E' : 250,
            'G' : 500,
            'H' : 630
        },
        'size_thickness' : {
            '3' : '0.3 mm',
            '5' : '0.5 mm',
            '8' : '0.8 mm',
            'A' : '0.65 mm',
            'C' : '0.85 mm',
            'F' : '1.25 mm',
            'H' : '1.6 mm'
        }
    }

    result = {k:lookups.get(k, {}).get(v, v) for k, v in matchgroup.items()}
    result['manufacturer'] = 'Samsung'
    result['capacitance'] = capcode_to_value(matchgroup['capacitance'])
    return(result)


# TDK ceramic capacitors
# TODO: add parser for CGA/CEU (automotive) series (https://product.tdk.com/info/en/catalog/datasheets/mlcc_automotive_general_en.pdf)
cap_tdk_gp_re = re.compile(
    '^(?P<manufacturer_series>C)'
    '(?P<case_package>[0-9]{4})'
    '(?P<dielectric_characteristic>CH|C0G|JB|X5R|X6S|X7R|X7S|X7T|X8R)'
    '(?P<voltage_rating_dc>[0-3][A-W])'
    '(?P<capacitance>[R0-9]{3})'
    '(?P<capacitance_tolerance>[A-Z])'
    '(?P<size_thickness>[0-9]{3})'
    '(?P<packaging_code>[A-Z])?'
    '(?P<control_code>[A-Z])?'
)

def cap_tdk_gp_parse(matchgroup):
    lookups = {
        'case_package': {
            '0603' : '0201',
            '1005' : '0402',
            '1608' : '0603',
            '2012' : '0805',
            '3216' : '1206',
            '3225' : '1210',
            '4532' : '1812'
        },
        'dielectric_characteristic' : {
            'C0G' : 'C0G/NP0',
            'X5R' : 'X5R',
            'X7R' : 'X7R'
        },
        'voltage_rating_dc' : {
            '0G' : 4,
            '0J' : 6.3,
            '1A' : 10,
            '1C' : 16,
            '1E' : 25,
            '1V' : 35,
            '1H' : 50,
            '2A' : 100,
            '2D' : 200,
            '2E' : 250,
            '2H' : 500,
            '2J' : 630
        },
        'capacitance_tolerance' : {
            'W' : '±0.05pF',
            'B' : '±0.1pF',
            'E' : '±0.2pF',
            'C' : '±0.25pF',
            'D' : '±0.5pF',
            'F' : '1%',
            'G' : '2%',
            'J' : '5%',
            'K' : '10%',
            'M' : '20%'
        },
        'size_thickness' : {
            '020' : '0.2 mm',
            '030' : '0.3 mm',
            '045' : '0.45 mm',
            '050' : '0.5 mm',
            '055' : '0.55 mm',
            '060' : '0.6 mm'
        }
    }

    result = {k:lookups.get(k, {}).get(v, v) for k, v in matchgroup.items()}
    result['manufacturer'] = 'TDK'
    result['capacitance'] = capcode_to_value(matchgroup['capacitance'])
    return(result)


# Kemet ceramic capacitors
cap_kemet_re = re.compile(
    '^C'
    '(?P<case_package>[0-9]{4})'
    '(?P<manufacturer_series>C|H|X|S|Y)'
    '(?P<capacitance>[R0-9]{3})'
    '(?P<capacitance_tolerance>[B-M])'
    '(?P<voltage_rating_dc>[1-9A])'
    '(?P<dielectric_characteristic>H|G|R|P|U)'
    '(?P<reliability_code>[A-Z])?'
    '(?P<plating_code>[A-Z])?'
    '(?P<packaging_code>[A-Z]+)?'
)

def cap_kemet_parse(matchgroup):
    lookups = {
        # case_package is already in EIA units
        'capacitance_tolerance' : {
            'J' : '5%',
            'K' : '10%',
            'M' : '20%',
            'Z' : '+80/-20%'
        },
        'voltage_rating_dc' : {
            '7' : 4,
            '9' : 6.3,
            '8' : 10,
            '4' : 16,
            '3' : 25,
            '6' : 35,
            '5' : 50,
            '1' : 100,
            '2' : 200,
            'A' : 250
        },
        'dielectric_characteristic' : {
            'G' : 'C0G/NP0',
            'R' : 'X7R',
            'P' : 'X5R',
            'U' : 'Z5U',
            'H' : 'X8R'
        }
    }
    result = {k:lookups.get(k, {}).get(v, v) for k, v in matchgroup.items()}
    result['manufacturer'] = 'KEMET'
    result['capacitance'] = capcode_to_value(matchgroup['capacitance'])
    return(result)

# Yageo ceramic capacitors
cap_yageo_re = re.compile(
    '^(?P<manufacturer_series>CC|CL|CQ|SC|AC|CS)'
    '(?P<case_package>[0-9]{4})'
    '(?P<capacitance_tolerance>[A-Z])'
    '(?P<packaging_code>R|K|P|F|C)?'
    '(?P<dielectric_characteristic>NPO|NP0|X7R|X7S|X7T|X8R)'
    '(?P<voltage_rating_dc>[0-9A-Z])'
    '(?P<plating_code>B)'
    '(?P<process_code>B|N)'
    '(?P<capacitance>[R0-9]{3})'
)

def cap_yageo_parse(matchgroup):
    lookups = {
        # case_package is already in EIA units
        'capacitance_tolerance' : {
            'A' : '±0.05pF',
            'B' : '±0.1pF',
            'C' : '±0.25pF',
            'D' : '±0.5pF',
            'F' : '1%',
            'G' : '2%',
            'J' : '5%',
            'K' : '10%',
            'M' : '20%',
            'Z' : '+80/-20%'
        },
        'dielectric_characteristic' : {
            'NPO' : 'C0G/NP0'
            # other values go right through
        },
        'voltage_rating_dc' : {
            '4' : 4,
            '5' : 6.3,
            '6' : 10,
            '7' : 16,
            '8' : 25,
            'G' : 35,
            '9' : 50,
            '0' : 100,
            'A' : 200,
            'Y' : 250,
            'B' : 500,
            'Z' : 630
        }
    }
    result = {k:lookups.get(k, {}).get(v, v) for k, v in matchgroup.items()}
    result['manufacturer'] = 'Yageo'
    result['capacitance'] = capcode_to_value(matchgroup['capacitance'])
    return(result)

# AVX ceramic capacitors
cap_avx_re = re.compile(
    '^(?P<case_package>[0-9]{4})'
    '(?P<voltage_rating_dc>[1-9A-Z])'
    '(?P<dielectric_characteristic>[A-Z])'
    '(?P<capacitance>[R0-9]{3})'
    '(?P<capacitance_tolerance>[B-Z])'
    '(?P<reliability_code>A|4)'
    '(?P<plating_code>T|U|X|Z|1|7)'
    '(?P<packaging_code>2|4|U)?'
    '(?P<special_code>[A-Z0-9])?'
)

def cap_avx_parse(matchgroup):
    lookups = {
        # case_package is already in EIA units
        'voltage_rating_dc' : {
            '4' : 4,
            '6' : 6.3,
            'Z' : 10,
            'Y' : 16,
            '3' : 25,
            'D' : 35,
            '5' : 50,
            '1' : 100,
            '2' : 200,
            '7' : 500,
        },
        'dielectric_characteristic' : {
            'A' : 'C0G/NP0',
            'C' : 'X7R',
            'D' : 'X5R',
            'F' : 'X8R',
            'G' : 'Y5V',
            'W' : 'X6S',
            'Z' : 'X7S'
        },
        'capacitance_tolerance' : {
            'B' : '±0.1pF',
            'C' : '±0.25pF',
            'D' : '±0.5pF',
            'F' : '1%',
            'G' : '2%',
            'J' : '5%',
            'K' : '10%',
            'M' : '20%',
            'Z' : '+80/-20%'
        }
    }
    result = {k:lookups.get(k, {}).get(v, v) for k, v in matchgroup.items()}
    result['manufacturer'] = 'AVX'
    result['capacitance'] = capcode_to_value(matchgroup['capacitance'])
    return(result)

# Taiyo Yuden ceramic capacitors
cap_taiyoyuden_re = re.compile(
    '^(?P<voltage_rating_dc>[A-U])'
    '(?P<manufacturer_series>M|V|W)'
    '(?P<plating_code>K|S)'
    '(?P<case_package>[0-9]{3})'
    '(?P<dimensional_tolerance_code>A|B|C)?'
    '(?P<dielectric_characteristic>BJ|B7|C6|C7|LD|CG|UJ|UK|SL|SD)'
    '(?P<capacitance>[R0-9]{3})'
    '(?P<capacitance_tolerance>[A-Z])'
    '(?P<size_thickness>[A-Z])'
    '(?P<special_code>[A-Z-])?'
    '(?P<packaging_code>F|T|P|R|W)?'
)

def cap_taiyoyuden_parse(matchgroup):
    lookups = {
        'voltage_rating_dc' : {
            'P' : 2.5,
            'A' : 4,
            'J' : 6.3,
            'L' : 10,
            'E' : 16,
            'T' : 25,
            'G' : 35,
            'U' : 50,
            'H' : 100,
            'Q' : 250,
            'S' : 630
        },
        'case_package': {
            '063' : '0201',
            '105' : '0402',
            '107' : '0603',
            '212' : '0805',
            '316' : '1206',
            '325' : '1210',
            '432' : '1812'
        },
        'dielectric_characteristic' : {
            'BJ' : 'X5R',
            'B7' : 'X7R',
            'C6' : 'X6S',
            'C7' : 'X7S',
            'CG' : 'C0G/NP0',
            'UJ' : 'U2J'
        },
        'capacitance_tolerance' : {
            'A' : '±0.05pF',
            'B' : '±0.1pF',
            'C' : '±0.25pF',
            'D' : '±0.5pF',
            'F' : '1%',
            'G' : '2%',
            'J' : '5%',
            'K' : '10%',
            'M' : '20%',
            'Z' : '+80/-20%'
        },
        'size_thickness' : {
            'K' : '0.125 mm',
            'H' : '0.13 mm',
            'C' : '0.2 mm',
            'D' : '0.2 mm',
            'P' : '0.3 mm',
            'T' : '0.3 mm',
            'K' : '0.45 mm',
            'V' : '0.5 mm',
            'W' : '0.5 mm',
            'A' : '0.8 mm',
            'D' : '0.85 mm'
        }
    }
    result = {k:lookups.get(k, {}).get(v, v) for k, v in matchgroup.items()}
    result['manufacturer'] = 'Taiyo Yuden'
    result['capacitance'] = capcode_to_value(matchgroup['capacitance'])
    return(result)


cap_parsers = [
    (cap_murata_re, cap_murata_parse),
    (cap_samsung_re, cap_samsung_parse),
    (cap_tdk_gp_re, cap_tdk_gp_parse),
    (cap_kemet_re, cap_kemet_parse),
    (cap_yageo_re, cap_yageo_parse),
    (cap_avx_re, cap_avx_parse),
    (cap_taiyoyuden_re, cap_taiyoyuden_parse)
]

def parse_mpn(mpn):
    for regex, fun in cap_parsers:
        a = regex.match(mpn)
        if a:
            return fun(a.groupdict())
