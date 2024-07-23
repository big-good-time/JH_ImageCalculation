import json

class DataModel():
    def __init__(self):
        self.readData()
        
    def readData(self):
        with open('./data.json', 'r') as f:
            self.data = json.load(f)
    
    def updateData(self):
        with open('./data.json', 'w') as f:
            json.dump(self.data, f)
    