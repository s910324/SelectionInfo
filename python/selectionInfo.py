
# Enter your Python code here

def x():
        mainWindow    = pya.Application.instance().main_window()
        layoutView    = mainWindow.current_view()  
        cellView      = layoutView.active_cellview() 
        layout        = cellView.layout()
        unit          = layout.dbu
        selInstArray  = []
        selShapeDict  = {}
        
        for o in layoutView.each_object_selected():
            oTrans      = o.trans()
            oX          = oTrans.disp.x
            oY          = oTrans.disp.y
            oR          = oTrans.rot()
            oM          = oTrans.is_mirror()
                
            if o.is_cell_inst():
                inst        = o.inst()
                cell        = inst.cell
                cellBox     = cell.bbox()
                cellName    = cell.name
                
                iTrans      = inst.trans
                iR          = inst.cplx_trans.angle
                iX          = iTrans.disp.x
                iY          = iTrans.disp.y
                na          = inst.na
                nb          = inst.nb
                a           = inst.da
                b           = inst.db
                fTrans      = (oTrans * iTrans)
                fX          = fTrans.disp.x
                fY          = fTrans.disp.y
                

                cellWidth, cellHeight = round(cellBox.width(), 6), round(cellBox.height(), 6)
                cellP1x,   cellP1y    = round(cellBox.p1.x,    6), round(cellBox.p1.y,     6)
                cellP2x,   cellP2y    = round(cellBox.p2.x,    6), round(cellBox.p2.y,     6)
                
                if (cellP1x,cellP1y)==(0, 0) :  
                    cellOrigin = "Lower Left"
                    
                elif (cellP1x,cellP1y)==(0, -cellHeight/2) :  
                    cellOrigin = "Center Left"     
                        
                elif (cellP1x,cellP1y)==(0, -cellHeight) :  
                    cellOrigin = "Upper Left"
                    
                elif (cellP1x,cellP1y)==(-cellWidth/2, 0) :  
                    cellOrigin = "Lower Center"
                    
                elif (cellP1x,cellP1y)==(-cellWidth/2, -cellHeight/2) :  
                    cellOrigin = "Center"     
                        
                elif (cellP1x,cellP1y)==(-cellWidth/2, -cellHeight) :  
                    cellOrigin = "Upper Center"
                         
                elif (cellP1x,cellP1y)==(-cellWidth, 0) :  
                    cellOrigin = "Lower Right"
                    
                elif (cellP1x,cellP1y)==(-cellWidth, -cellHeight/2) :  
                    cellOrigin = "Center Right"     
                        
                elif (cellP1x,cellP1y)==(-cellWidth, -cellHeight) :  
                    cellOrigin = "Upper Right"    
                else:
                    cellOrigin = "Non Standard"
                    result["Warning"].append("Non-standard Cell origin")
                
                info        = {
                    "cellName"   : cellName,
                    "isPcell"    : inst.is_pcell(),
                    "width"      : "%.3f" % (cellWidth  * unit),
                    "height"     : "%.3f" % (cellHeight * unit),
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
                    "arrayCount" : "%d"   % (na*nb),
                    "cell_LB"    : f"({cellP1x}, {cellP1y})",
                    "cell_RT"    : f"({cellP2x}, {cellP2y})",
                    "cell_center": cellOrigin,
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
                    if shape.is_text()    : 
                    
                        print (f"{oX * unit}, {oY * unit}, {shape.dtext.string}")
                        selShapeDict[layerStr]["Text"]    += 1     
                    
x()