import requests
import xmltodict
import sqlite3
from datetime import datetime



response = requests.get('https://knesset.gov.il/Odata/ParliamentInfo.svc/KNS_Status')
data = xmltodict.parse(response.content)


db = sqlite3.connect("db_kns.db")
cursur = db.cursor()
print(data['feed']['entry'][4]['content']['m:properties'])


for entry in range(len(data['feed']['entry'])):
    entry = int(entry)
    dict_data = data['feed']['entry'][entry]['content']['m:properties']
    status = dict_data['d:StatusID']['#text']

    desc = str(dict_data['d:Desc'])
    if isinstance(dict_data['d:Desc'], dict) and '#text' in dict_data['d:Desc']:
        desc = str(dict_data['d:Desc']['#text'])

    typeID = dict_data['d:TypeID']['#text']
    orderTransition = 0
    if dict_data['d:OrderTransition']['@m:null'] == 'true':
        orderTransition = 1

    isActive = False
    if dict_data['d:OrderTransition']['@m:null'] == 'true':
        isActive = True

    date_time = dict_data['d:LastUpdatedDate']['#text'].split('T')
    date_time = datetime.strptime(date_time[0], '%Y-%m-%d')

    cursur.execute('''INSERT INTO KNS_Status(StatusID, Desc, TypeID, TypeDesc, OrderTransition, IsActive, LastUpdatedDate)
                        VALUES(:StatusID, :Desc, :TypeID, :TypeDesc, :OrderTransition, :IsActive, :LastUpdatedDate)''',
                   {'StatusID': status, 'Desc': desc, 'TypeID': typeID,
                    'TypeDesc': dict_data['d:TypeDesc'], 'OrderTransition': orderTransition,
                    'IsActive': isActive, 'LastUpdatedDate': date_time})


cursur.execute('''SELECT * FROM KNS_Status''')
for row in cursur:
    print(row)