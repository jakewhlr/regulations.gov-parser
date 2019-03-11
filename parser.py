#!/usr/bin/env python3

import requests, csv, time, sys, json

api_key = '23jOs9uefHRVxsHzKbAP7kGBAi9S5LGlOYAJMrZx'
docket_id = 'ED-2018-OCR-0064'
total_docs = 32068
docs_per_page = 1000
requests_list = []
parsed_list = []

for i in range(int(total_docs / docs_per_page)):
    parsed_list.append(json.loads(requests.get("https://api.data.gov:443/regulations/v3/documents.json",
                     params={
                             "api_key": api_key,
                             "dktid": docket_id,
                             "rpp": docs_per_page,
                             "po": i * docs_per_page,
                    }).content))

fieldnames = ['author', 'datetime', 'comment']
with open('output.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for page in parsed_list:
        for comment in page['documents']:
            dict_line = {'author': None, 'datetime': None, 'comment': None}

            if 'submitterName' in comment.keys():
                dict_line['author'] = comment['submitterName']

            if 'postedDate' in comment.keys():
                dict_line['datetime'] = comment['postedDate']

            if 'commentText' in comment.keys():
                dict_line['comment'] = comment['commentText']

            writer.writerow(dict_line)
