from api import vkapi as vk
from collections import Iterable
from cfgreader import readConfig, configElem

import re, json, random, csv
from pathlib import Path

cfg = readConfig("profile_cfg.json")

silent = False

def profiles(ids, fields = cfg.fields):
    if isinstance(fields,Iterable): fields = ",".join(fields)
    if isinstance(ids,Iterable): ids = ",".join(ids)
    return configElem(vk.users.get(user_ids = ids, fields = fields))

def randprofs(count = 100, splitBy = 100, filterDeact = True):
    if not splitBy: splitBy = 2**32
    result = []
    selected = set()
    while len(result) < count:
        pack = min(count - len(result), splitBy)
        if not silent:
            print("getting another chunk of records... ", end = "")
            before = len(result)
        ids = set(str(random.randint(cfg.id_range.low ,cfg.id_range.high)) for i in range(pack)).difference(selected)
        profs = None
        while not profs:
            try:
                profs = profiles(ids)
            except Exception: pass
            
        if filterDeact: profs = [p for p in profs if "deactivated" not in p]
        result.extend(profs)
        selected.update(str(p["id"]) for p in profs)
        if not silent:
            print(str(len(result)-before) + "records get")
    return configElem(result)

def trans(s):
	print(json.dumps(dict(zip(count(1),re.findall("[a-zA-Z][a-zA-Z ]*",s))),indent=True))

def flat(profile):
    res = {"id": profile.id, "sex": cfg.sex[str(profile.sex)]}
    for name in cfg.personal:
        if "personal" in profile and name in profile.personal:
            res[name] = cfg.personal[name][str(profile.personal[name])]
        else: res[name] = "not specified"
    return res

header = ["id","sex"]
header.extend(cfg.personal.keys())

def dumpRandCSV(file = "sex.csv", *args, **kw):
    profs = randprofs(*args,**kw)
    with open(file,"wt") as fp:
        writer = csv.DictWriter(fp,header,dialect="unix")
        writer.writeheader()
        writer.writerows(map(flat,profs))
       
    
