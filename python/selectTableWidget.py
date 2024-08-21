import pya

class SelectTableWidget(pya.QTableWidget):
    def __init__(self, data = [], headers = [], parent = None):
        super(SelectTableWidget, self).__init__()  
        self.setEditTriggers(pya.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(pya.QAbstractItemView.SelectRows)
        self.data    = data
        self.headers = headers
        self.setData(data, headers)
 
    def setData(self, data = [], headers = []):
        self.clearContents()
        self.data    = data
        self.headers = headers
        
        self.setRowCount(len(data))
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        #print("\n")
        print(", ".join(headers))
        print("\n".join([ ", ".join([str(v) for k, v in row.items()]) for row in data]))
        
        for column in range(len(headers)):
            if column == 0:
                self.setColumnWidth(column, 165)
            else:
                self.setColumnWidth(column, 85)
                
        for row, instData in enumerate(data):
            for column, header in enumerate(headers):
                dataStr = str(instData[header])
                item    = pya.QTableWidgetItem(dataStr)
                item.setTextAlignment(2)
                self.setItem (row, column, item )
                
        

    def clearContents(self):
        self.data    = []
        self.headers = []        
        super(SelectTableWidget, self).clearContents()
        
        

