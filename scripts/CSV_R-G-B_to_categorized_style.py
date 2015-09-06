##Style=group
##CSV R-G-B to categorized style=name

##Vector_layer=vector 
##Value_field=field Vector_layer
##CSV_file_with_semicolon_delimiter= file
##CSV_Encoding=string latin1
##Column_value=number 0
##Column_label=number 1
##Column_red=number 2
##Column_green=number 3
##Column_blue=number 4
##Transparency=number 0.50
##Outline=boolean false
##Outline_width=number 0.26
##Save_layer_style_as_default=boolean false

from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import csv
import codecs
import os

layer = processing.getObject(Vector_layer)

filePth = layer.dataProvider().dataSourceUri()
myDirectory,nameFile = os.path.split(filePth)
nomCouche = str(os.path.splitext(os.path.split(filePth)[1])[0])

# Verifie l'extension du fichier demande : CSV
fileName, fileExtension = os.path.splitext(CSV_file_with_semicolon_delimiter)
if  fileExtension =='.csv':
    # Ouverture du csv
    read_csv = csv.reader(open(CSV_file_with_semicolon_delimiter,"r"),delimiter=";")
    #Permet de passer l'entete du CSV
    read_csv.next()
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Creation d'un tableau qui va stocker les lignes et colonnes choisies du CSV  
    tab = []
    if Column_value >= 0 and  Column_label>= 0 and Column_red >= 0 and Column_green >= 0 and Column_blue >= 0 and Transparency>=0 and Transparency<=1 and Outline_width >0:
        for row in read_csv:
            # Permet de definir les colonnes value, label, red, green, blue
            col_select =row[Column_value], row[Column_label].decode(CSV_Encoding),row[Column_red], row[Column_green], row[Column_blue]
            # Insere chaque ligne du CSV dans le tableau
            tab.append(col_select)
            
            #Permet la suppression des doublons
            Lt= list(set(tab))
            Lt.sort()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        categories = []
        for value, label, red, green, blue in Lt :
            #Concatener r,g,b
            color_rgb = red+','+green+','+blue
            tab_list = value +' - '+label+' - '+red+','+green+','+blue
            progress.setText(u'Category : %s' % tab_list)
            # Creation de la ligne
            if Outline == False :
               b_outline = 'no'
            else :
                b_outline = 'yes'
            # Largeur de la ligne
            v_width = str(Outline_width)

            # Polygon
            if layer.wkbType()==QGis.WKBPolygon25D or layer.wkbType()==QGis.WKBPolygon or layer.wkbType()==QGis.wkbMultiPolygon or layer.wkbType()==QGis.wkbMultiPolygon25D:
                # Source : http://gis.stackexchange.com/questions/53121/how-change-border-line-to-no-pen-with-python-console
                symbol = QgsFillSymbolV2.createSimple( {'style':'solid','outline_style':b_outline,'outline_width':v_width,'color':color_rgb} )
                symbol.setAlpha (Transparency)
                    
                category = QgsRendererCategoryV2(value, symbol, label)
                categories.append(category)

            # Line
            if layer.wkbType()==QGis.WKBLineString25D or layer.wkbType()==QGis.WKBLineString or layer.wkbType()==QGis.WKBMultiLineString or layer.wkbType()==QGis.WKBMultiLineString25D:
                symbol = QgsLineSymbolV2.createSimple( {'style':'solid','line_width':v_width,'color': color_rgb} )
                symbol.setAlpha (Transparency)
                    
                category = QgsRendererCategoryV2(value, symbol, label)
                categories.append(category)

            # Point
            if layer.wkbType()==QGis.WKBPoint25D or layer.wkbType()==QGis.WKBPoint or layer.wkbType()==QGis.WKBMultiPoint or layer.wkbType()==QGis.WKBMultiPoint25D:     
                symbol = QgsMarkerSymbolV2.createSimple( {'style':'solid','outline_style':'no','outline_width':v_width,'color': color_rgb} )
                symbol.setAlpha (Transparency)
                    
                category = QgsRendererCategoryV2(value, symbol, label)
                categories.append(category)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Permet de creer le rendu et de l'affecter a la couche sur un champ defini
        
        # Nom du champ sur lequel doit s'appliquer la symbologie
        expression = Value_field

        renderer = QgsCategorizedSymbolRendererV2(expression, categories)
        layer.setRendererV2(renderer)
        
        # Creation des fichiers de style
        if Save_layer_style_as_default :
            # QML
            layer.saveDefaultStyle() 
            # SLD
            #layer.saveSldStyle(myDirectory+'/'+nomCouche+'.sld')
            
            progress.setText(u'QML is created')
                
        iface.messageBar().pushMessage("Information :", "Process is done!", QgsMessageBar.INFO, duration=5)
        
        iface.mapCanvas().refresh()
        layer.triggerRepaint() 
    else :
        iface.messageBar().pushMessage("Warning :", "Problem of value", QgsMessageBar.WARNING, duration=15)
        
else :
    iface.messageBar().pushMessage("Warning :", "CSV is required!", QgsMessageBar.WARNING, duration=15)
