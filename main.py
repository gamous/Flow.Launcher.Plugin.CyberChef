import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher
import webbrowser
import base64,json,os
from functools import cached_property

class CyberChef(FlowLauncher):

    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    

    @cached_property
    def plugindir(self):
        potential_paths = [
            os.path.abspath(os.getcwd()),
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        ]
        for path in potential_paths:
            while True:
                if os.path.exists(os.path.join(path, 'plugin.json')):
                    return path
                elif os.path.ismount(path):
                    return os.getcwd()
                path = os.path.dirname(path)

    @cached_property
    def settings(self):
        app_data=os.path.dirname(os.path.dirname(self.plugindir))
        app_setting=os.path.join(app_data, 'Settings',"Plugins", self.__class__.__name__,'Settings.json')
        with open(app_setting, 'r') as f:
            return json.load(f)

    def query(self, query):
        self.site_url = self.settings.get("site_url")
        self.query_string=query
        if self.site_url==None or self.site_url=="":
            self.site_url="https://gchq.github.io/CyberChef"
        return [
            {
                "title": "Input: {}".format(( query , query)[query == '']),
                "subTitle": "Press enter to open in CyberChef",
                "icoPath": "Images/app.png",
                "jsonRPCAction": {
                    "method": "open_url",
                    "parameters": [self.site_url+"/#input={}".format(base64.b64encode(query.encode()).decode())],
                },
                "contextData":[query],
                "score": 0
            }
        ]

    def context_menu(self, data):
        self.site_url = self.settings.get("site_url")
        if self.site_url==None or self.site_url=="":
            self.site_url="https://gchq.github.io/CyberChef"
        if data==None:
            data=""
        else:
            data=data[0]
        return [
            {
                "title": "To Base64",
                "subTitle": "Base64 encode",
                "icoPath": "Images/app.png",
                "jsonRPCAction": {
                    "method": "open_url",
                    "parameters": [self.site_url+"/#recipe=To_Base64('A-Za-z0-9%2B/%3D')&input="+base64.b64encode(data.encode()).decode().strip('=')]
                },
                "score" : 0
            },
            {
                "title": "From Base64",
                "subTitle": "Base64 decode",
                "icoPath": "Images/app.png",
                "jsonRPCAction": {
                    "method": "open_url",
                    "parameters": [self.site_url+"/#recipe=From_Base64('A-Za-z0-9%2B/%3D')&input="+base64.b64encode(data.encode()).decode().strip('=')]
                },
                "score" : 0
            }
        ]

    def open_url(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    CyberChef()