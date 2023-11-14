import json
from tokenize import Name



newintents = dict({'intent':[]})
intentlist = list()

with open('medicine2.json','r+') as f :
    data = json.load(f)
    for i in data["intent"]:
        number = i['Medicine_Number']
        Uses = i['Uses']
        Prescription = i['Prescription']
        MRP = i['MRP']
        name = i['Medicine Name'][0].replace("-"," ")
        finalname = list()
        finalname += [name]
        print(type(name))
        print(finalname)
        splitnamel = list()
        splitnamel.extend(finalname)
        print(splitnamel)
        
        sname = finalname[0].split()
        
        splitnamel.extend(sname)
        splitnames = " ".join(splitnamel)
        intentdict = {"Medicine_Number":i['Medicine_Number'],"Medicine Name":splitnamel,"Uses":i['Uses'],"Prescription":i['Prescription'],"MRP":i['MRP']}
        intentlist.append(intentdict)
newintents["intent"] = intentlist

with open("medicine2.json", "w") as outfile:
    json.dump(newintents, outfile)
    

    
