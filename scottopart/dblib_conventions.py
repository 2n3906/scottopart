#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Altium Database Library (DbLib) conventions belong here."""

__author__ = 'Scott Johnston'
__version__ = '0.0.1'

import math
from UliEngineering import EngineerIO

tablenames_from_octopart_categories = {
    'e7ca2ac0de173c0d': 'Capacitors - Aluminum Electrolytic',
    'f6473b4dcf9d2d80': 'Capacitors - Ceramic',
    'd820152ae1f903e7': 'Capacitors - Polymer',
    '75fab8f04590ae3d': 'Connectors',
    '008acd80318bdb4d': 'Crystals',
    '87a44aaeb6be5c63': 'Diodes',
    '1af2d7f82326c135': 'Diodes',  # TVS diodes
    '7bf8b6f24b72a03f': 'Fuses',
    '531c9e16639788db': 'Fuses',
    'f5f838f2cc2f2e3f': 'Fuses',  # PTC
    'c67d0b77f76a1dba': 'Inductors - Ferrite Bead',
    '8ef743fdbff05530': 'Inductors - Fixed',
    '9e07530daf1645c0': 'Integrated Circuits',
    '0c13c1193cf8d7d4': 'Integrated Circuits',  # optocouplers
    '1a30d73a2e7bc1f7': 'Integrated Circuits',  # protection ICs
    '0dd3c0d93d8cd614': 'LEDs',
    '0111cc1b3285dad6': 'Relays',
    'a2f46ffe9b377933': 'Resistors - Chip',
    '01fbccf130c0da3c': 'Resistors - Thermistor',
    '8ce341e9bf4c5724': 'Switches',
    'a91d6417981872da': 'Transformers',  # CM chokes actually
    '244ee944154dff89': 'Transformers',
    'd77d1a77e69f0cba': 'Transistors',
    'd6c01bcae73c0d07': 'Varistors'
}

parttypes_from_octopart_categories = {
    'e7ca2ac0de173c0d': 'Capacitor',
    'f6473b4dcf9d2d80': 'Capacitor',
    'd820152ae1f903e7': 'Capacitor',
    '75fab8f04590ae3d': 'Connector',
    '008acd80318bdb4d': 'Crystal',
    '87a44aaeb6be5c63': 'Diode',
    '1af2d7f82326c135': 'Diode',  # TVS diodes
    '7bf8b6f24b72a03f': 'Fuse',
    '531c9e16639788db': 'Fuse',
    'f5f838f2cc2f2e3f': 'Fuse',  # PTC
    'c67d0b77f76a1dba': 'Inductor',
    '8ef743fdbff05530': 'Inductor',
    '9e07530daf1645c0': 'Integrated Circuit',
    '0c13c1193cf8d7d4': 'Integrated Circuit',  # optocouplers
    '1a30d73a2e7bc1f7': 'Integrated Circuit',  # protection ICs
    '0dd3c0d93d8cd614': 'LED',
    '0111cc1b3285dad6': 'Relay',
    'a2f46ffe9b377933': 'Resistor',
    '01fbccf130c0da3c': 'Resistor',
    '8ce341e9bf4c5724': 'Switch',
    'a91d6417981872da': 'Transformer',  # CM chokes actually
    '244ee944154dff89': 'Transformer',
    'd77d1a77e69f0cba': 'Transistor',
    'd6c01bcae73c0d07': 'MOV'
}

table_fields_shared = ['Manufacturer',
                       'MPN',
                       'Comment',
                       'Description',
                       'PartNumber',
                       'Value',
                       'Library Path',
                       'Library Ref',
                       'Footprint Path',
                       'Footprint Ref',
                       'Supplier 1',
                       'Supplier Part Number 1',
                       'ComponentLink1Description',
                       'ComponentLink1URL']
table_fields = {
    'Capacitors - Aluminum Electrolytic': table_fields_shared + ['Capacitance', 'Capacitance Tolerance', 'Equivalent Series Resistance (ESR)', 'Case/Package', 'Case/Package (SI)', 'Dielectric Characteristic', 'Dielectric Material', 'Mounting Style', 'RoHS', 'Size-Diameter', 'Size-Height', 'Type', 'Voltage Rating'],
    'Capacitors - Ceramic': table_fields_shared + ['Capacitance', 'Capacitance Tolerance', 'Case/Package', 'Case/Package (SI)', 'Dielectric Characteristic', 'Dielectric Material', 'Mounting Style', 'RoHS', 'Size-Height', 'Size-Length', 'Size-Width', 'Type', 'Voltage Rating'],
    'Capacitors - Polymer': table_fields_shared + ['Capacitance', 'Capacitance Tolerance', 'Equivalent Series Resistance (ESR)', 'Case/Package', 'Case/Package (SI)', 'Dielectric Characteristic', 'Dielectric Material', 'Mounting Style', 'RoHS', 'Size-Diameter', 'Size-Height', 'Type', 'Voltage Rating'],
    'Inductors - Fixed': table_fields_shared + ['Case/Package', 'Case/Package (SI)', 'Current Rating', 'Inductance', 'Inductance Tolerance', 'Mounting Style', 'Q-Factor', 'RoHS', 'Self-Resonant Frequency', 'Shielding', 'Size-Height', 'Size-Length', 'Size-Width', 'Type'],
    'LEDs': table_fields_shared + ['Case/Package', 'Case/Package (SI)', 'Dielectric Characteristic', 'Color', 'Forward Voltage', 'Lens Type', 'Luminous Intensity', 'Mounting Style', 'RoHS', 'Size-Height', 'Size-Length', 'Size-Width', 'Type', 'Viewing Angle', 'Wavelength'],
    'Resistors - Chip': table_fields_shared + ['Case/Package', 'Case/Package (SI)', 'Composition', 'Mounting Style', 'Power Rating', 'Resistance', 'Resistance Tolerance', 'RoHS', 'Size-Height', 'Size-Length', 'Size-Width', 'Temperature Coefficient', 'Type', 'Voltage Rating']
}

def get_tablename(octopart_category_uids):
    """Determine correct SQL table name (or False) from Octopart category UID list."""
    return next((tablenames_from_octopart_categories[x] for x in octopart_category_uids if x in tablenames_from_octopart_categories), False)

def get_parttype(octopart_category_uids):
    """Determine correct part type (or False) from Octopart category UID list."""
    return next((parttypes_from_octopart_categories[x] for x in octopart_category_uids if x in parttypes_from_octopart_categories), False)

def get_tablefields(tablename):
    """Return header fields in correct sequence for Copy-Pasting."""
    return table_fields[tablename]

# Normalize descriptions for certain parts (resistors, capacitors)
# def normalize_description(part):

def split_valuestring(input):
    # Don't forget to handle '\u03a9'(capital omega) and '\u2126' (ohm sign)
    # And '\u03bc' (greek mu) and '\u00b5' (micro sign)
    a = EngineerIO.EngineerIO(units=frozenset(['A', 'Ω', 'Ω', 'F', 'H', 'V', 'W']),
                              suffices=[["y"], ["z"], ["a"], ["f"], ["p"], ["n"], ["\u00b5", "\u03bc", "u"], ["m"], [], ["k"], ["M"], ["G"], ["T"], ["E"], ["Z"], ["Y"]])
    # Return val, unit
    return a.safe_normalize(input)

def format_value(v, unit=''):
    """
    Format v using SI suffices with optional units.
    Suppress trailing zeros.
    """
    exp_suffix_map = {
        -5: 'f',
        -4: 'p',
        -3: 'n',
        -2: 'µ',
        -1: 'm',
        0: '',
        1: 'k',
        2: 'M',
        3: 'G',
    }
    #Suffix map is indexed by one third of the decadic logarithm.
    exp = 0 if v == 0. else math.log(abs(v), 10.)
    suffixMapIdx = int(math.floor(exp / 3.))
    #Ensure we're in range
    if not min(exp_suffix_map.keys()) < suffixMapIdx < max(exp_suffix_map.keys()):
        raise ValueError("Value out of range: {0}".format(v))
    #Pre-multiply the value
    v = v * (10.0 ** -(suffixMapIdx * 3))

    res = '{:.5g}'.format(v)
    suffix = exp_suffix_map[suffixMapIdx] + unit
    return "{0} {1}".format(res, suffix) if suffix else res

def standardize_description(table_name, table_row):
    try:
        if table_name == 'Resistors - Chip':
            return 'RES ' + table_row['Case/Package'] + ' ' + table_row['Resistance'].replace(' ', '') + ' ' + table_row['Resistance Tolerance'].replace(' ', '') + ' ' + table_row['Power Rating'].replace(' ', '')
        elif table_name == 'Capacitors - Ceramic':
            return 'CAP CER ' + table_row['Case/Package'] + ' ' + table_row['Capacitance'].replace(' ','')  + ' ' + table_row['Voltage Rating'].replace(' ', '') + ' ' + table_row['Dielectric Characteristic']
        elif table_name == 'Capacitors - Aluminum Electrolytic':
            return 'CAP ALUM ' + table_row['Capacitance'].replace(' ','')  + ' ' + table_row['Voltage Rating'].replace(' ', '') + ' ' + table_row['Equivalent Series Resistance (ESR)'].replace(' ', '')
        elif table_name == 'Capacitors - Polymer':
            return 'CAP POLY ' + table_row['Capacitance'].replace(' ','')  + ' ' + table_row['Voltage Rating'].replace(' ', '') + ' ' + table_row['Equivalent Series Resistance (ESR)'].replace(' ', '')
        elif table_name == 'LEDs':
            return 'LED ' + table_row['Case/Package'] + ' ' + table_row['Color'].upper()
        elif table_name == 'Inductors - Fixed':
            return 'IND ' + table_row['Inductance'].replace(' ', '') + ' ' + table_row['Current Rating'].replace(' ', '')
        elif 'Description' in table_row:
            return table_row['Description']
        else:
            return ''
    except KeyError:
        if 'Description' in table_row:
            return table_row['Description']
        else:
            return ''

def normalize_ratings(table_row):
    for field, unit in [['Resistance', '\u2126'], ['Capacitance', 'F'], ['Inductance', 'H'], ['Power Rating', 'W'], ['Voltage Rating', 'V'], ['Equivalent Series Resistance (ESR)', '\u2126']]:
        if field in table_row:
            v, u = split_valuestring(table_row[field])
            table_row[field] = format_value(v, unit)
    return table_row
