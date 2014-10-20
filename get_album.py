import json,os,re,csv

items = []
for name in os.listdir():
    if not re.match("data.*\.json",name): continue
    with open(name,encoding = "cp1251") as f:
        data = json.load(f)
        items.extend(data['response']['items'])

names = set()
        
for item in items:
    keysToDelete = []
    updItem = {}    
    for key in item:
        val = item[key]
        if isinstance(val,dict):
            keysToDelete.append(key)
            for subkey in val:
                updItem[key+"."+subkey] = val[subkey]
    item.update(updItem)
    for key in keysToDelete: del item[key]
    names.update(item.keys())
    
names = sorted(names)

with open("vk.csv","wt",encoding = 'cp1251') as f:
    writer = csv.DictWriter(f,names,dialect = "unix")
    writer.writeheader()
    writer.writerows(items)
