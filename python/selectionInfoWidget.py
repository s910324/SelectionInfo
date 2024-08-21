import pya
import selectTableWidget

class SelectionInfoWidget(pya.QWidget):
    def __init__(self, parent = None):
        super(SelectionInfoWidget, self).__init__()  

        self.selInstWidget  = selectTableWidget.SelectTableWidget()
        self.selShapeWidget = selectTableWidget.SelectTableWidget()
        self.instGB         = pya.QGroupBox("Selected Instances")
        self.shapeGB        = pya.QGroupBox("Selected Shapes")
        self.instLY         = pya.QVBoxLayout()
        self.shapeLY        = pya.QVBoxLayout()
        self.refreshPB      = pya.QPushButton("refresh")
        self.donePB         = pya.QPushButton("done")
        self.layout         = pya.QGridLayout()
        self.split          = pya.QSplitter()
        
        self.instGB.setLayout(self.instLY)
        self.shapeGB.setLayout(self.shapeLY)
        self.instLY.addWidget(self.selInstWidget)
        self.shapeLY.addWidget(self.selShapeWidget)
        self.split.addWidget(self.instGB)
        self.split.addWidget(self.shapeGB)
        self.split.setOrientation(pya.Qt.Vertical)
        
        self.layout.addWidget(self.split,          0,0,1,3)
        self.layout.addWidget(self.refreshPB,      1,1,1,1)
        self.layout.addWidget(self.donePB,         1,2,1,1)
        self.layout.setColumnStretch(0, 1) 
        
        self.refreshPB.clicked(lambda : self.setData())
        self.donePB.clicked(lambda : self.close())        
        self.setLayout(self.layout)
        self.resize(1000, 600)
        self.setData()
        self.setWindowTitle ("Selection Information")
        
    def setData(self):
        shapeHeaders        = ["layer", "Box", "Polygon", "Path", "Shapes", "rawArea", "mergedArea"]                
        instHeaders         = ["cellName", "isPcell", "width", "height", "x", "y", "rotation", "mirror", "row", "column", "row_dx", "row_dy", "column_dx", "column_dy", "arrayCount"]
        instData, shapeData = self.selectedItems()
        self.selInstWidget.setData(instData, instHeaders)
        self.selShapeWidget.setData(shapeData, shapeHeaders)


    def selectedItems(self):
        mainWindow    = pya.Application.instance().main_window()
        layoutView    = mainWindow.current_view()  
        cellView      = layoutView.active_cellview() 
        layout        = cellView.layout()
        unit          = layout.dbu
        selInstArray  = []
        selShapeDict  = {}
        
        for o in layoutView.each_object_selected():
            if o.is_cell_inst():
                inst        = o.inst()
                cell        = inst.cell
                cellBox     = cell.bbox()
                cellName    = cell.name
                cellwidth   = cellBox.width()
                cellheight  = cellBox.height()
                
                iTrans      = inst.trans
                iR          = inst.cplx_trans.angle
                iX          = iTrans.disp.x
                iY          = iTrans.disp.y
                oTrans      = o.trans()
                oX          = oTrans.disp.x
                oY          = oTrans.disp.y
                oR          = oTrans.rot()
                oM          = oTrans.is_mirror()
                na          = inst.na
                nb          = inst.nb
                a           = inst.da
                b           = inst.db
                fTrans      = (oTrans * iTrans)
                fX          = fTrans.disp.x
                fY          = fTrans.disp.y

                info        = {
                    "cellName"   : cellName,
                    "isPcell"    : inst.is_pcell(),
                    "width"      : "%.3f" % (cellwidth  * unit),
                    "height"     : "%.3f" % (cellheight * unit),
                    "x"          : "%.3f" % (fX         * unit),
                    "y"          : "%.3f" % (fY         * unit),
                    "rotation"   : "%.3f" % iR,
                    "mirror"     : "%s"   % oM,
                    "row"        : "%d"   % na,
                    "column"     : "%d"   % nb,
                    "row_dx"     : "%.3f" % a.x,
                    "row_dy"     : "%.3f" % a.y,
                    "column_dx"  : "%.3f" % b.x,
                    "column_dy"  : "%.3f" % b.y,
                    "arrayCount" : "%d"   % (na*nb)
                }
                selInstArray.append(info)
                
            else:
                shape     = o.shape
                layerInfo = shape.layer_info
                layerStr  = f"{layerInfo.layer}/{layerInfo.datatype}"
        
                if not(layerStr in selShapeDict):
                    selShapeDict[layerStr] = {
                        "layer"      : layerStr,
                        "Box"        : 0,
                        "Polygon"    : 0,
                        "Path"       : 0,
                        "Text"       : 0,
                        "Shapes"     : 0,
                        "rawArea"    : 0,
                        "mergedArea" : 0,
                        "collect"    : pya.Shapes()
                    }
                if shape.polygon:
                    if shape.is_box()     : selShapeDict[layerStr]["Box"]     += 1
                    if shape.is_polygon() : selShapeDict[layerStr]["Polygon"] += 1
                    if shape.is_path()    : selShapeDict[layerStr]["Path"]    += 1
                
                    selShapeDict[layerStr]["Shapes"]   += 1
                    selShapeDict[layerStr]["rawArea"]  += shape.polygon.area()
                    selShapeDict[layerStr]["collect"].insert(shape.polygon.transformed(o.trans())) 
                    
                else:
                    if shape.is_text()    : selShapeDict[layerStr]["Text"]    += 1       
            
        for key in selShapeDict:
            region = pya.Region().insert(selShapeDict[key]["collect"])
            selShapeDict[key]["mergedArea"] = f'{region.merged().area()*unit*unit:.6f}'
            selShapeDict[key]["rawArea"]    = f'{selShapeDict[key]["rawArea"]*unit*unit:.6f}'
            selShapeDict[key]["Box"]        = f'{selShapeDict[key]["Box"]:d}'
            selShapeDict[key]["Polygon"]    = f'{selShapeDict[key]["Polygon"]:d}'
            selShapeDict[key]["Path"]       = f'{selShapeDict[key]["Path"]:d}'
            selShapeDict[key]["Text"]       = f'{selShapeDict[key]["Text"]:d}'
            selShapeDict[key]["Shapes"]     = f'{selShapeDict[key]["Shapes"]:d}'  
        selShapeArray = [selShapeDict[key] for key in selShapeDict]
            
        return selInstArray, selShapeArray
        
    def keyPressEvent(self, event):
        if event.type() == pya.QEvent.KeyPress:
            if event.key() in (pya.Qt.Key_Return, pya.Qt.Key_Escape):
                self.close()