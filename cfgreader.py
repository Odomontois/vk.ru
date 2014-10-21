from collections import UserDict, UserList
from collections.abc import Mapping, Sequence

class ConfigDict(UserDict):
    """Config dictionaries with access to options as attributes"""
    def __getattr__(self,name):
        return configElem(self.data[name])
    def __setattr__(self,name,value):
        if name == "data": self.__dict__["data"] = value
        else: self.data[name] = value

class ConfigList(UserList):
    """Config lists with for config wrapper"""
    def __getitem__(self,item):
        return configElem(self.data[item])

def configElem(elem):
    if isinstance(elem,(str,int,float,bool)): return elem
    if isinstance(elem,Mapping): return ConfigDict(elem)
    if isinstance(elem, Sequence): return ConfigList(elem)
    return elem

def readConfig(file, cfgtype = None):
    if cfgtype is None and isinstance(file, str):
         cfgtype = file.split(".")[-1]
    with open(file) as fp:
        if cfgtype == "json":
            import json
            return configElem(json.load(fp))
        


        
