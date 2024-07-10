import json
import pandas as pd
from lifelines import CoxPHFitter



##
# Read data from files and associate them with paths.
##
def readData():
    data = {}

    szz_f = open('./SZZ_data.json')
    code_smell_f = open('./project_code_smells.json')

    szz_data = json.load(szz_f)
    code_smell_data = json.load(code_smell_f)

    for item in szz_data:
        path = item['path']
        if path not in data:
            data[path] = {"time":item['time'], 'smells':[]}
        else:
            data[path]['time'] = item['time']    

    for item in code_smell_data:
        path = item['path']
        if path not in data:
            data[item['path']] = {"time":None, 'smells':item['smells']}
        else:
            data[path]['smells'] = item["smells"]   
    return data



def formatData():
    data = readData()
    time = []
    smells = []
    event =[]
    for path, info in data.items():
        time.append(info['time']) if info['time'] is not None else time.append(0)
        smells.append(1) if len(info['smells']) >0  else smells.append(0)

        if info['time'] is not None and len(info['smells']) >0:
            event.append(1)
        else:
            event.append(0)    
        
    cox_data = {
        'time' : time,
        'smells':smells,
        'event':event
    }
    print("Length of each array : " )
    print("Time: " + str(len(time)) +" Smells: " + str(len(smells)) + " Event: " + str(len(event)) )
    print(cox_data)
    return cox_data




def COX_model():

    data = formatData()

    df = pd.DataFrame(data)

    cox = CoxPHFitter()
    cox.fit(df, duration_col='time', event_col='event', formula='smells')
    cox.print_summary()   
    
COX_model()