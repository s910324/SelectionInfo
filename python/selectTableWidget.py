import pya

class SelectTableWidget(pya.QTableWidget):
    def __init__(self, data = [], headers = [], parent = None):
        super(SelectTableWidget, self).__init__()  
        self.setEditTriggers(pya.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(pya.QAbstractItemView.SelectItems)
        self.data    = data
        self.headers = headers
        self.setData(data, headers)
        
    def keyPressEvent(self, event):
        self.copyTable()
    
    def copyTable(self):
        copyText    = ''
        copiedCells = sorted(self.selectedIndexes())
        maxColumn   = copiedCells[-1].column()
        maxRow      = copiedCells[-1].row()
               
        for c in copiedCells:
            cellText = self.item(c.row(), c.column()).text
            copyText += cellText
            if c.column() == maxColumn:
                if c.row() != maxRow:
                    copyText += '\n'
            else:
                copyText += '\t'
        pya.QApplication.clipboard().setText(copyText)
        pya.QToolTip.showText(pya.QCursor.pos, "Information Copied to Clipboard")
        
    def setData(self, data = [], headers = []):
        self.clearContents()
        self.data    = data
        self.headers = headers
        
        self.setRowCount(len(data))
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        #print("\n")
        #print(", ".join(headers))
        #print("\n".join([ ", ".join([str(v) for k, v in row.items()]) for row in data]))
        
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
                
    def copyTable(self):
        copyText    = ''
        copiedCells = sorted(self.selectedIndexes())
        maxColumn   = copiedCells[-1].column()
        maxRow      = copiedCells[-1].row()
               
        for c in copiedCells:
            cellText = self.item(c.row(), c.column()).text
            copyText += cellText
            if c.column() == maxColumn:
                if c.row() != maxRow:
                    copyText += '\n'
            else:
                copyText += '\t'
        pya.QApplication.clipboard().setText(copyText)

    def clearContents(self):
        self.data    = []
        self.headers = []        
        super(SelectTableWidget, self).clearContents()
        
        

    def keyPressEvent(self, event):
        #super().keyPressEvent(event)
        self.copyTable()

if __name__ == "__main__": 
    view = pya.Application.instance().main_window().current_view()
    liw  = SelectTableWidget()
    liw.show()