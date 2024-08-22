import pya

class LayerIconWidget(pya.QWidget):
    def __init__(self, view, parent = None):
        super(LayerIconWidget, self).__init__()
        self.view   = view  
        self.layout = pya.QVBoxLayout()
        self.setLayout(self.layout)     

    def getLayerIcon(self, layerIndex = []):
        bgc  = self.view.get_config("background-color")
        txtc = "#FFFFFF" if (int(bgc[1:3], 16) + int(bgc[3:5], 16) + int(bgc[5:7], 16)) <= (255) else "#000000"
        itr  = self.view.begin_layers()
        
        while not(itr.at_end()):
            lyp = itr.current()
            if (lyp.layer_index() in layerIndex or layerIndex == []):
                layerPixmap = pya.QPixmap()
                layerImage  = pya.QLabel(self)
                nameLabel   = pya.QLabel(self)
                sourceLabel = pya.QLabel(self)
                layerLabel  = pya.QLabel(self)
                layerLayout = pya.QHBoxLayout(self)
                
    
                layerLabel.setText(f"{lyp.source_layer}/{lyp.source_datatype}")
                sourceLabel.setText(f"@{lyp.source_cellview + 1}")
                nameLabel.setText(f"{lyp.source_name}")
                
    
                layerPixmap.loadFromData(self.view.icon_for_layer(itr, 25, 10, 1).to_png_data())
                layerImage.setPixmap(layerPixmap)
    
                for labelSet in [[sourceLabel, 20],  [layerLabel, 35], [nameLabel, 65]]:
                    labelSet[0].setStyleSheet("color:%s;" % txtc)
                    labelSet[0].setFixedWidth(labelSet[1])
                    
                for widget in [layerImage, sourceLabel, layerLabel, nameLabel]:
                    layerLayout.addWidget(widget)                
    
                
                layerLayout.addStretch()
                self.layout.addLayout(layerLayout)
            itr.next()
            
        self.setStyleSheet("background-color:%s;" % bgc)
        self.update()

        
        
if __name__ == "__main__": 
    view = pya.Application.instance().main_window().current_view()
    liw  = LayerIconWidget(view)
    liw.show()
 