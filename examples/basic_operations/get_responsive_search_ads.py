#!/usr/bin/env python
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example gets non-removed responsive search ads in a specified ad group.

To add responsive search ads, run basic_operations/add_responsive_search_ad.py.
To get ad groups, run basic_operations/get_ad_groups.py.
"""

import argparse
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, page_size, ad_group_id=None):
    ga_service = client.get_service('GoogleAdsService', version='v2')

    query = ('SELECT ad_group.id, ad_group_ad.ad.id, '
             'ad_group_ad.ad.expanded_text_ad.headline_part1, '
             'ad_group_ad.ad.expanded_text_ad.headline_part2, '
             'ad_group_ad.status FROM ad_group_ad '
             'WHERE ad_group_ad.ad.type = EXPANDED_TEXT_AD')

    if ad_group_id:
        query = '%s AND ad_group.id = %s' % (query, ad_group_id)

    results = ga_service.search(customer_id, query=query, page_size=page_size)

    try:
        for row in results:
            ad = row.ad_group_ad.ad

            if ad.expanded_text_ad:
                expanded_text_ad_info = ad.expanded_text_ad

            print('Expanded text ad with ID %s, status %s, and headline '
                  '%s - %s was found in ad group with ID %s.'
                  % (ad.id, row.ad_group_ad.status,
                     expanded_text_ad_info.headline_part1,
                     expanded_text_ad_info.headline_part2,
                     row.ad_group.id))
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='List ad groups for specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-a', '--ad_group_id', type=str,
                        required=False, help='The ad group ID. ')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, _DEFAULT_PAGE_SIZE,
         ad_group_id=args.ad_group_id)
