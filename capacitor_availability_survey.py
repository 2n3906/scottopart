#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Just a little python script."""

__author__ = 'Scott Johnston'
__version__ = '0.0.1'

import sys
import os
import csv
import argparse
import requests
import time

######## EDIT BELOW THIS LINE ############

# authorized_capacitor_manufacturers = ['TDK', 'Murata', 'Yageo', 'KEMET']
# authorized_resistor_manufacturers = ['Yageo', 'Panasonic', 'Vishay']
authorized_sellers = ['Digi-Key', 'Newark', 'Mouser', 'Avnet', 'Arrow Electronics, Inc.']
authorized_country_codes = ['US']
authorized_packaging = ['Cut Tape', 'Tape & Reel', 'None']

e3 = [1.0, 2.2, 4.7]
e6 = [1.0, 1.5, 2.2, 3.3, 4.7, 6.8]
e12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
e24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                  3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
standard_capacitor_values_below_1uF = [round(i * 1e-12, 13) for i in e6] + \
    [round(i * 1e-11, 12) for i in e24] + \
    [round(i * 1e-10, 12) for i in e24] + \
    [round(i * 1e-9, 12) for i in e24] + \
    [round(i * 1e-8, 12) for i in e24] + \
    [round(i * 1e-7, 12) for i in e12]

standard_capacitor_values_above_1uF = [round(i * 1e-6, 12) for i in e3] + \
    [round(i * 1e-5, 12) for i in e3] + \
    [100e-6]

all_capacitor_values = standard_capacitor_values_below_1uF + standard_capacitor_values_above_1uF

case_packages = ['0603']

key_specs = ['capacitance', 'capacitance_tolerance', 'case_package', 'dielectric_characteristic', 'operating_temperature', 'voltage_rating_dc']

csv_fieldnames = [
    'query_case_package',
    'query_capacitance',
    'brand',
    'mpn',
    'octopart_url',
    'total_in_stock',
    'capacitance',
    'capacitance_tolerance',
    'case_package',
    'dielectric_characteristic',
    'min_operating_temperature',
    'max_operating_temperature',
    'voltage_rating_dc'
]

######## EDIT ABOVE THIS LINE ############

def search_octopart_capacitors(case_package, capacitance):
    octopart_api_key = os.environ['OCTOPART_API_KEY']
    url = "http://octopart.com/api/v3/parts/search"
    payload = {
        'apikey': octopart_api_key,
        'q': '', # leave blank
        'filter[fields][manufacturer.displayname][]': ['TDK', 'Murata', 'Yageo', 'KEMET'],
        'filter[fields][specs.capacitance.value][]': capacitance,
        'filter[fields][specs.case_package.value][]': case_package,
        'limit' : 100,
        'include[]' : 'specs',
    }
    r = requests.get(url, params=payload)
    return r.json()

def json_results_to_list(json):
    solutions = []
    for item in json['results']:
        authorized_offers = [x for x in item['item']['offers'] if x['seller']['display_flag'] in authorized_country_codes and x['seller']['name'] in authorized_sellers and x['packaging'] in authorized_packaging]
        total_in_stock = sum([x['in_stock_quantity'] for x in authorized_offers])
        part = {
            'brand' : item['item']['brand']['name'],
            'mpn' : item['item']['mpn'],
            'octopart_url' : item['item']['octopart_url'],
            'total_in_stock' : total_in_stock,
        }
        filtered_specs = {k:v for (k,v) in item['item']['specs'].items() if k in key_specs}
        if 'operating_temperature' in filtered_specs:
            filtered_specs['min_operating_temperature'] = {'value': [filtered_specs['operating_temperature']['min_value']]}
            filtered_specs['max_operating_temperature'] = {'value': [filtered_specs['operating_temperature']['max_value']]}
            filtered_specs.pop('operating_temperature', None)
        for spec, val in filtered_specs.items():
            if val['value']:
                part[spec] = val['value'][0]
            else:
                part[spec] = None
        solutions.append(part)
    return solutions

def main(output_file=False):
    """Main screen turn on."""

    writer = csv.DictWriter(output_file, fieldnames=csv_fieldnames)
    writer.writeheader()

    for case_package in case_packages:
        for val in all_capacitor_values:
            json_result = search_octopart_capacitors(case_package, val)
            solutions = json_results_to_list(json_result)
            for s in solutions:
                row = s
                row['query_capacitance'] = val
                row['query_case_package'] = case_package
                writer.writerow(row)
            output_file.flush()
            time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    #parser.add_argument('infile', help="Input file", type=argparse.FileType('r'))
    parser.add_argument('-o', '--outfile', help="Output file",
                        default=sys.stdout, type=argparse.FileType('w'))
    args = parser.parse_args()

    main(args.outfile)
