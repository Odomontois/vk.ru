import vk, json, time, csv, webbrowser
from urllib.parse import urlparse, parse_qs
from datetime import datetime as dt

cfg = json.load(open("cfg.json"))

scope = cfg["scope"]
params = cfg["params"]
params["scope"] = ",".join(k for k in scope if scope[k])
url = "https://oauth.vk.com/authorize?"+"&".join("%s=%s" % (k,params[k]) for k in params)

def accessDialog():
    import tkinter as tk
    class AccessAsker(tk.Frame):
        def __init__(self, master = None):
            tk.Frame.__init__(self,master)
            self.pack()
            self.visualize()
            
        def visualize(self):
            self.ok = tk.Button(self)
            self.ok["text"] = "OK"
            self.ok["command"] = self.enter
            self.ok.pack(side="bottom")

            self.urlLabel = tk.LabelFrame(self, text = "paste URL here",)
            self.urlLabel.pack(side = "top")

            self.urlField = tk.Entry(self.urlLabel)
            self.urlField.pack()

            self.passLabel = tk.LabelFrame(self, text = "Enter your password")
            self.passLabel.pack(side = "top")
            
            self.passField = tk.Entry(self.passLabel, show = "*")
            self.passField.pack()
            
        def enter(self):
            self.password = self.passField.get()
            self.url = self.urlField.get()
            root.destroy()
            
    root = tk.Tk()
    asker = AccessAsker(master = root)
    asker.mainloop()
    return (asker.url, asker.password)   

def readAccess():
    access = {}
    webbrowser.open(url)    
    (redirUrl,password) = accessDialog()
    access = parse_qs(urlparse(redirUrl).fragment)
    access = dict((k,v[0]) for k,v in access.items())
    access["time"] = time.time()
    access["password"] = password
    json.dump(access,open("access.json","wt"),indent = True)
    return access

try:
    access = json.load(open("access.json"))
    if access["time"] <= time.time() - 24 * 60 * 60 : access = readAccess()
except FileNotFoundError:
    access = readAccess()    

vkapi = vk.API(app_id        = cfg["params"]["client_id"],
               user_login    = access["email"],
               user_password = access["password"],
               access_token  = access["access_token"])

