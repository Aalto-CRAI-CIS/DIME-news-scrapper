'''
This code is used to extract meta data which is not included in newspaper4k lib. The main metadata collected by this snippet is updatedDate or modifiedData
'''

import requests
import json

url = "https://www.is.fi//api/data-for-path/%2Fkuninkaalliset%2Fart-2000010241524.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Cookie": "sa1pid=9f3a1ffe-eb6c-4817-a3aa-264e6d5b3106; racID=c88c0a48-eb4c-4187-8cf3-18fdd0a3300c; _dd_s=logs=0&expire=1708456933984; _sp_su=false; euconsent-v2=CP6RzMAP6RzMAAGABBENAmEgAP_gAEPAAApAI3wLYAFAAYABAACoAFwAMgAcAA8ACAAGQANAAfQBEAEUAJMATABOACoAFsAL4AYQA_ACAAEEAIQAYIA0QB-gEIAIiARMAiwBHQCRAGKANMAdQBAoCNQEyAKsAWyAvMBjIDmgHxAP5AjeCYcAkAC4AMgBmgEIAIiAwQB8QEbwJhgDhIBwACwAKgAcAA8ACCAGQAaABEACYAH4AQgA_QCRAGKAXmOgJAALAAqABwAEEAMgA0ACIAEwAPwA0QB-gEWgI6AkQBigDqAJkAVYAtkBeZCAKAAsAJgBigDqAKsJQBwAFgAcACIAEwAxQB1AF5lICAACwAKgAcABAADQAIgATAA_ADRAH6ARaAjoCRAGKAOoAqwBeZQACAFstABAVYAA.f_gAAAAAAAAA; consentUUID=21ad958f-7582-49b3-b243-b637a91e292c_25_29; consentDate=2024-02-20T18:45:54.930Z"
}

r = requests.get(url=url, headers=headers)

with open("test.json", "w") as outfile:
    outfile.write(r.text)
    
print(r.json()['assetData']['displayDate'])
print()
print(r.json()['assetData']['sharingMetadata']['modifiedDate'])
