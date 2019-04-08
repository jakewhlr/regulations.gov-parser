#!/usr/bin/env python3
import requests, csv, time, sys, json, re, argparse
import logging as log
parser = argparse.ArgumentParser()
parser.add_argument("n_comments", type = int, help = "Number of comments to grab")
parser.add_argument('-v', '--verbose', action = 'count', default = 0)
args = parser.parse_args()

if args.verbose:
    log.basicConfig(format = "%(levelname)s: %(message)s", level = log.DEBUG)
    log.info("Verbose output.")
else:
    log.basicConfig(format = "%(levelname)s: %(message)s")


api_key = '23jOs9uefHRVxsHzKbAP7kGBAi9S5LGlOYAJMrZx'
docket_id = 'ED-2018-OCR-0064'
total_docs = args.n_comments
docs_per_page = 1000
requests_list = []
parsed_list = []
states = []

regex_string = '^(.+),(.+) (\d{5})$'

for i in range(int(total_docs / docs_per_page)):
    log.info("Getting page " + str(i))
    parsed_list.append(json.loads(requests.get("https://api.data.gov:443/regulations/v3/documents.json",
                     params={
                             "api_key": api_key,
                             "dktid": docket_id,
                             "rpp": docs_per_page,
                             "po": i * docs_per_page,
                    }).content))


fieldnames = ['author', 'datetime', 'comment', 'state']
with open('output.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i, page in enumerate(parsed_list):
        for j, comment in enumerate(page['documents']):
            log.info("Parsing page " +  str(i) + " comment " + str(j))
            dict_line = {'author': None, 'datetime': None, 'comment': None}
            if 'submitterName' in comment.keys():
                dict_line['author'] = comment['submitterName']

            if 'postedDate' in comment.keys():
                dict_line['datetime'] = comment['postedDate']

            if 'commentText' in comment.keys():
                dict_line['comment'] = comment['commentText']
                match = re.search(regex_string, comment['commentText'], re.MULTILINE)
                if match:
                    dict_line['state'] = match.group()
            writer.writerow(dict_line)