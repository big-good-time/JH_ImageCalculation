import json

class DataModel():
    def __init__(self):
        self.readData()
        
    def readData(self):
        try:
            with open('./data.json', 'r') as f:
                self.data = json.load(f)
        except:
            self.initData()
    
    def updateData(self):
        with open('./data.json', 'w') as f:
            json.dump(self.data, f)

    def initData(self):
        """重置配置文件"""
        self.data = {"black_down_price": "0.3", "black_up_price": "0.1", "color_down_price": "0.5", "color_up_price": "0.2", "style_sheet": "./Style\\Ubuntu.qss"}
        self.updateData()
    