#!/usr/bin/env python3

import requests, csv, time, sys, json, re

api_key = '23jOs9uefHRVxsHzKbAP7kGBAi9S5LGlOYAJMrZx'
docket_id = 'ED-2018-OCR-0064'
total_docs = 53000
docs_per_page = 1000
requests_list = []
parsed_list = []
states = []
# regex_string = '(\d+)(.+)\n((.)+),(.+) (\d{5})(-(\d{4}))?'
regex_string = '(Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New\sHampshire|New\sJersey|New\sMexico|New\sYork|North\sCarolina|North\sDakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode\sIsland|South\sCarolina|South\sDakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West\sVirginia|Wisconsin|Wyoming)|(A[LKZR])|((C[AOT])|(D[EC])|(FL)|(GA)|(HI)|(I[DLNA])|(K[SY])|(LA)|(M[EDAINSOT])|(N[EVHJMYCD])|(O[HKR])|(PA)|(RI)|(S[CD])|(T[NX])|(UT)|(V[TA])|(W[AVIY]))'

for i in range(int(total_docs / docs_per_page)):
    print("Getting page", i)
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
            print("Parsing page", i, " comment", j)
            dict_line = {'author': None, 'datetime': None, 'comment': None}
            if 'submitterName' in comment.keys():
                dict_line['author'] = comment['submitterName']
                # print(comment['submitterName'])

            if 'postedDate' in comment.keys():
                dict_line['datetime'] = comment['postedDate']

            if 'commentText' in comment.keys():
                dict_line['comment'] = comment['commentText']
                match = re.search(regex_string, comment['commentText'])
                if match:
                    matches = match.groups()
                    filtered = filter(None, matches)
                    states = []
                    for state in filtered:
                        states.append(state)
                    dict_line['state'] = states[0]
            writer.writerow(dict_line)