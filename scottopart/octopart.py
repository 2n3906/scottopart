import sys
import os
import argparse
from pyoctopart.octopart import Octopart
import pprint
from .dblib_conventions import get_tablename, get_parttype, normalize_ratings, standardize_description

class Scottopart:
    def __init__(self):
        try:
            self.octopart_api_key = os.environ['OCTOPART_API_KEY']
        except KeyError:
            print('Missing OCTOPART_API_KEY environment variable.')
            sys.exit(1)
        self.octopart = Octopart(apikey=self.octopart_api_key)


    def match_by_mpn(self, mpn):
        """Lookup a list of MPNs in Octopart."""
        if not isinstance(mpn, (list, tuple)):
            # If called with a single string, return a scalar instead of a list.
            return self.match_by_mpn([mpn])[0]
        octopart_results = []
        for i in range(0, len(mpn), 20):
            batched_mpns = mpn[i: i + 20]
            batched_queries = [{'mpn': x, 'seller': 'Digi-Key', 'limit': 1} for x in batched_mpns]
            result = self.octopart.parts_match(queries=batched_queries,
                                               exact_only=True,
                                               include_short_description=True,
                                               include_specs=True,
                                               include_category_uids=True)
            octopart_results.extend(result[0]['results'])
        # Now process the items in octopart_results
        scottopart_results = []
        for i, r in enumerate(octopart_results):
            if r['hits'] == 0:
                # This query returned no results!
                scottopart_results.append({'query_mpn': mpn[i],
                                           'success': False})
            else:
                table_name = get_tablename(r['items'][0]['category_uids'])
                table_row = {}
                table_row['Manufacturer'] = r['items'][0]['manufacturer']['name'].title() # fix capitalization
                table_row['MPN'] = r['items'][0]['mpn']
                table_row['Description'] = r['items'][0]['short_description']
                table_row['ComponentLink1Description'] = 'Octopart'
                table_row['ComponentLink1URL'] = r['items'][0]['octopart_url']
                table_row['Type'] = get_parttype(r['items'][0]['category_uids'])
                # Check for non-active lifecycle status.
                if 'lifecycle_status' in r['items'][0]['specs'] and 'display_value' in r['items'][0]['specs']['lifecycle_status']:
                    if r['items'][0]['specs']['lifecycle_status']['display_value'] != 'Active':
                        table_row['Comment'] = 'WARNING: Lifecycle Status is ' + r['items'][0]['specs']['lifecycle_status']['display_value']
                authorized_suppliers = ['Digi-Key', 'Mouser']
                filtered_offers = [x for x in r['items'][0]['offers'] if x['seller']['name'] in authorized_suppliers]
                # Check for low in_stock_quantity.
                if max([x['in_stock_quantity'] for x in filtered_offers]) < 500:
                    table_row['Comment'] = 'WARNING: LOW STOCK'
                # Pick a supplier part number.
                for offer in r['items'][0]['offers']:
                    if offer['seller']['name'] == 'Digi-Key' and offer['packaging'] == 'Cut Tape':
                        table_row['Supplier 1'] = 'Digi-Key'
                        table_row['Supplier Part Number 1'] = offer['sku']
                # Fill in all the component specs.
                for key, value in r['items'][0]['specs'].items():
                    if 'display_value' in value:
                        table_row[value['metadata']['name']] = value['display_value']
                # Fix up some field names.
                if 'Voltage Rating (DC)' in table_row:
                    table_row['Voltage Rating'] = table_row.pop('Voltage Rating (DC)')
                # Normalize ratings (eliminate trailing zeroes, use correct Unicode character for unit, etc.)
                table_row = normalize_ratings(table_row)
                # Standardize Description field for certain part types.
                table_row['Description'] = standardize_description(table_name, table_row)

                scottopart_results.append({'query_mpn': mpn[i],
                                           'success': True,
                                           'table_name': table_name,
                                           'table_row': table_row
                })
        return scottopart_results
