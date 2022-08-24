import pandas as pd
import json
 
with open('vaccine_data.json') as json_file:
    data = json.load(json_file)

new=[]
for i in range(len(data['vaccine_data'])):
    curr=data['vaccine_data'][i]
    new.extend(curr)

pd.DataFrame.from_records(new).drop(columns=['action']).to_csv('vaksin.csv.gz',index=None)
