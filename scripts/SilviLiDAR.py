
##carpeta=folder
##crecimiento=number 1.5
##fccbaja=number 20.0
##fccterrazas=number 57.5
##fccmedia=number 46.0
##fccalta=number 95.0
##hmontebravoe=number 3.5
##hmontebravo=number 5.0
##hselvicolas=number 7.5
##hclaras=number 12.0
##hclaras2=number 16.5
##hbcminima=number 3.0
##hbcdesarrollado=number 5.5
##rcclaras=number 35.0
##rcextremo=number 17.0
##longitudcopaminima=number 3.25
##crecimientofcc=number 12.5

import os
import glob
import re
import sys

from qgis.core import *
import qgis.utils
from qgis.utils import iface
from qgis.core import QgsProject
from PyQt4.QtCore import QFileInfo
from qgis.gui import *
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from math import *
import processing

from PyQt4.QtCore import *
from PyQt4.QtGui import *

#compruebo que capas estan cargadas en el proyecto al iniciar el script
capasoriginales =QgsMapLayerRegistry.instance().mapLayers()

a=["nombre de archivo","extension"]

#congelo la vista  para ahorrar memoria
canvas = iface.mapCanvas()
canvas.freeze(True)

#defino la funcion que busca los archivos las o laz que existan y le paso los parametros resultantes del formulario
def buscalidaryejecuta(carpeta, crecimiento, fccbaja, fccterrazas, fccmedia, fccalta, hmontebravoe, hmontebravo, hselvicolas, hclaras, hclaras2, hbcminima, hbcdesarrollado, rcclaras, rcextremo, longitudcopaminima, crecimientofcc):
    for base, dirs, files in os.walk(carpeta):
        carpetas_y_subcarpetas=base
        archivos=files
        for archivo in archivos:
            a=list(os.path.splitext(archivo))
            extension=a[1].lower()
            print extension
            if extension==".laz" or extension==".las":
                b=os.path.join(base,a[0]+a[1])
                las = os.path.join(a[0]+a[1])
                #ejecuto el exprimelidar
                exprimelidar(las, carpeta, crecimiento, fccbaja, fccterrazas, fccmedia, fccalta, hmontebravoe, hmontebravo, hselvicolas, hclaras, hclaras2, hbcminima, hbcdesarrollado, rcclaras, rcextremo, longitudcopaminima, crecimientofcc)
                
#defino la funcion que lo hace todo con un archivo las o laz concreto
def exprimelidar(las, carpeta, crecimiento, fccbaja, fccterrazas, fccmedia, fccalta, hmontebravoe, hmontebravo, hselvicolas, hclaras, hclaras2, hbcminima, hbcdesarrollado, rcclaras, rcextremo, longitudcopaminima, crecimientofcc):
    fcstring = ""
    
    #defino un par de variables con el nombre del archivo y su abreviatura. Pensado para la denominacion estandar de los archivos LiDAR del PNOA
    tronco=las[:-4]
    troncoresumido=las[24:27]+"_"+las[28:32]
    
    #definicion de parametros funciones y rutas
    funcion1 = "c:/fusion/groundfilter"
    funcion2 = "c:/fusion/gridsurfacecreate"
    funcion3 = "c:/fusion/gridmetrics"
    funcion4 = "c:/fusion/csv2grid"
    funcion6 = "c:/fusion/DTM2ASCII"
    funcion7 = "c:/Fusion/LDA2ASCII"

    salida0 =  os.path.join(carpeta,a[0]+ ".las")
    salida00 =  os.path.join(carpeta,"filt"+a[0]+ ".las")
    salida1 = os.path.join(carpeta,"groundfilter_"+tronco+".lda")
    salida2 = os.path.join(carpeta,"groundfilter_"+tronco+".dtm")
    salida6 = os.path.join(carpeta,"groundfilter_"+tronco+".las")
    salida3 = os.path.join(carpeta,"metric.csv")
    salida4 = os.path.join(carpeta,tronco+"_height_grid.asc")
    salida5 = os.path.join(carpeta,tronco+"_cover_grid.asc")
    salida7 = os.path.join(carpeta,tronco+"_height.txt")
    salida8 = os.path.join(carpeta,tronco+"_height_grid_original.asc")
    salida100=os.path.join(carpeta,tronco+"_basecopa.asc")
    
    parametros1 = 10
    parametros1_0 = "" #"/median:3 /wparam:2.5 /aparam:4 /bparam:4"
    parametros2= "10 M M 0 0 0 0"
    parametros3_1 = "/minht:2 /nointensity" 
    parametros3_2 = "0.5 10"
    parametros4 = 7
    parametros5 = 49
    parametros6 = "/raster"
    parametro7 = 2
    parametros100 = 27 #percentil del 20 por ciento
    parametros104 = 37 #percentil del 95 por ciendto
    
    entrada0 = os.path.join(carpeta,las)
    entrada1 = os.path.join(carpeta,las) 
    entrada2 = os.path.join(carpeta,"groundfilter_"+tronco+".las")
    entrada3_1 = salida2
    entrada3_2 = entrada1
    entrada4 = os.path.join(carpeta,"metric_all_returns_elevation_stats_"+tronco+".csv")
    entrada6 = salida2

    try:
        while True:
            #paso1 groundfilter
            total1 = funcion1+" "+parametros1_0+" "+salida1+" "+str(parametros1)+" "+ entrada1   
            os.system(total1)

            #paso2 grid del suelo
            total2 = funcion2+" "+salida2+" "+str(parametros2)+" "+ entrada2
            os.system(total2)

            #paso3 saca los parametros de ese grid
            total3 = funcion3+" "+str(parametros3_1)+" "+entrada3_1+" "+str(parametros3_2)+" "+salida3+" "+ entrada3_2
            os.system(total3)
            os.rename(carpeta+"/metric_all_returns_elevation_stats.csv", carpeta+"/metric_all_returns_elevation_stats_"+tronco+".csv")
            os.rename(carpeta+"/metric_all_returns_elevation_stats_ascii_header.txt", carpeta+"/metric_all_returns_elevation_stats_"+tronco+"_ascii_header.txt")

            #paso4 genera un grid del csv anterior  de alturas
            total4 = funcion4+" "+entrada4+" "+str(parametros104)+" "+ salida4
            os.system(total4)
          
            #paso100 percentil20
            total100 = funcion4+" "+entrada4+" "+str(parametros100)+" "+ salida100
            os.system(total100)

            #paso5 genera un grid del csv anterior de fcc
            total5 = funcion4+" "+entrada4+" "+str(parametros5)+" "+ salida5
            os.system(total5)
            
            #paso6 convierto en ascii 
            total6 = funcion6+" "+str(parametros6)+" "+entrada6
            os.system(total6)
            
            #paso7  convierto en ascii
            total7 = funcion7+" "+entrada1+" "+salida7+" "+str(parametro7)
            os.system(total7)
                      
            #cargo  raster fcc
            fileName=salida5
            Layer= QgsRasterLayer(fileName,"fcc")
            QgsMapLayerRegistry.instance().addMapLayers([Layer])
            if not Layer:
                print "fallo carga de capa" 
            
            #creo lista vacia entries
            entries = []
 
            #funcion que carga una capa y prepara la banda para operar con ella
            def StringToRaster(raster,banda):
                fileInfo = QFileInfo(raster)
                path = fileInfo.filePath()
                baseName = fileInfo.baseName()
                global layerglobal
                layerglobal = QgsRasterLayer(path, baseName)
                QgsMapLayerRegistry.instance().addMapLayer(layerglobal)
                if layerglobal.isValid() is True:
                    bandaref=str(banda)+'@1'
                    # Define band1
                    banda = QgsRasterCalculatorEntry()
                    banda.ref = bandaref
                    banda.raster = layerglobal
                    banda.bandNumber = 1
                    entries.append( banda )
                else:
                    print "Unable to read basename and file path - Your string is probably invalid" +str(baseName)
                    
            #defino funcion para hacer calculo de capas raster        
            def calculo(expresion,capa):
                calc = QgsRasterCalculator(expresion, 
                                os.path.join(carpeta,troncoresumido+'_'+capa+'.tif'), 
                                'GTiff', 
                                layerglobal.extent(), 
                                layerglobal.width(), 
                                layerglobal.height(), 
                                entries )
                                 
                calc.processCalculation()
                del(calc)
                
                
            #defino funcion para crear una capa shape que generalice los datos de un raster    
            def agregado(rasterdeentrada):
                #filtro gausian para dar valor en funcion de los vecinos
                input=os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'1.tif')
                sigma=0.2
                mode=1
                radius=2
                result=os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'g2.tif')
                processing.runalg('saga:gaussianfilter', input, sigma, mode, radius, result)
                StringToRaster(os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'g2.tif'),rasterdeentrada+str("g2"))
                
                #filtro y me quedo con lo mayor de 0,40
                calc = QgsRasterCalculator("'"+rasterdeentrada+'g2@1 > 0.40',
                                           os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'g2s.tif'),
                                           'GTiff',
                                    layerglobal.extent(), 
                                    layerglobal.width(), 
                                    layerglobal.height(), 
                                    entries )
                calc.processCalculation()
                del(calc)
                StringToRaster(os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'g2s.tif'),rasterdeentrada+str("g2s"))
                
                #convierto en nodata lo que no me interesa
                calc = QgsRasterCalculator(("'"+rasterdeentrada+'g2s@1'>0)*"'"+rasterdeentrada+'g2s@1', 
                            os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'g2sn.tif'), 
                            'GTiff', 
                            layerglobal.extent(), 
                            layerglobal.width(), 
                            layerglobal.height(), 
                            entries )
                calc.processCalculation()
                del(calc)
                StringToRaster(os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'g2sn.tif'),rasterdeentrada+str("g2sn"))
               
                #filtro  filter clums eliminar los huecos menores de 1300 m2
                input=os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'g2sn.tif')  
                threshold=13
                result=os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'3.tif')
                processing.runalg('saga:filterclumps', input, threshold, result)
                StringToRaster(os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'3.tif'),rasterdeentrada+str("3"))

                #filtro mayorityffilter para dar valor en funcion de los vecinos
                input=os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'3.tif')
                mode=0
                radius=1
                threshold=4
                result=os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'4.tif')
                try:
                    processing.runalg('saga:majorityfilter', input, mode, radius, threshold, result)
                    StringToRaster(os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'4.tif'),rasterdeentrada+str("4"))
                    
                    #filtro para rellenar huecos pequenos
                    input=os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'4.tif')
                    distance=3
                    iterations=0
                    band=1
                    mask=None
                    no_default_mask='True'
                    output=os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'5.tif')
                    processing.runalg('gdalogr:fillnodata', input, distance, iterations, band,mask,no_default_mask, output)
                    StringToRaster(os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'5.tif'),rasterdeentrada+str("5"))

                    #filtro  filter clums eliminar los huecos
                    input=os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'5.tif')

                    threshold=5
                    result=os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'6.tif')
                    processing.runalg('saga:filterclumps', input, threshold, result)
                    StringToRaster(os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'6.tif'),rasterdeentrada+str("6"))

                    #filtro para rellenar huecos pequenos
                    input=os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'6.tif')
                    distance=3
                    iterations=0
                    band=1
                    mask=None
                    no_default_mask='True'
                    output=os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'7.tif')
                    processing.runalg('gdalogr:fillnodata', input, distance, iterations, band,mask,no_default_mask, output)
                    StringToRaster(os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'7.tif'),rasterdeentrada+str("7"))
                    
                    #lo vectorizo
                    processing.runalg("gdalogr:polygonize",os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'7.tif'),"DN",os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'.shp'))

                    #seleciono lo que me interesa
                    lyr=QgsVectorLayer(os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'.shp'),rasterdeentrada,"ogr")
                    QgsMapLayerRegistry.instance().addMapLayers([lyr])
                    selection = lyr.getFeatures(QgsFeatureRequest().setFilterExpression(u'"DN" = 1'))
                    selecionado = lyr.setSelectedFeatures([s.id() for s in selection])
                    nbrSelected=lyr.selectedFeatureCount()

                    if nbrSelected > 0:
                        #guardo lo selecionado
                        processing.runalg("qgis:saveselectedfeatures",os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'.shp'),os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'2.shp'))

                        #calcula la superficie de esta capa pero no en todos los registros
                        layer=QgsVectorLayer(os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'2.shp'),rasterdeentrada+str("2"),"ogr")
                        provider = layer.dataProvider()
                        areas = [ feat.geometry().area()  for feat in layer.getFeatures() ]
                        indice = [ feat.id()  for feat in layer.getFeatures() ]
                        field = QgsField("area", QVariant.Int)
                        provider.addAttributes([field])
                        layer.updateFields()
                        idx = layer.fieldNameIndex('area')
                        long=len(indice)
                        i=0
                        while i<long:
                            new_values = {idx : float(areas[i])}
                            provider.changeAttributeValues({indice[i]:new_values})
                            i=i+1           
                        layer.updateFields()

                        #selecciono las teselas mayor de una superficie dada.
                        layer2=QgsVectorLayer(os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'2.shp'),rasterdeentrada+str("2"),"ogr")
                        QgsMapLayerRegistry.instance().addMapLayers([layer2])
                        selection = layer2.getFeatures(QgsFeatureRequest().setFilterExpression(u'"area" > 2500'))
                        selecionado = layer2.setSelectedFeatures([s.id() for s in selection])
                    
                        #guardo lo selecionado
                        processing.runalg("qgis:saveselectedfeatures",os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'2.shp'),os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'3.shp'))
                        layer3=QgsVectorLayer(os.path.join(carpeta,troncoresumido+'_'+rasterdeentrada+'3.shp'),rasterdeentrada+str("3"),"ogr")
                        QgsMapLayerRegistry.instance().addMapLayer(layer3)
                        del(selection)
                        del(selecionado)
                        
                except:
                    pass
          
            #calculo las variables basicas sin proyectar
            StringToRaster(salida5,"fcc")
            calculo('fcc@1',"fcc")
            StringToRaster(salida4,"hm")
            calculo('hm@1',"hm")
            StringToRaster(salida100,"hbc")
            calculo('hbc@1',"hbc")
            calculo('100 * ( hm@1 - hbc@1 ) / hm@1',"rc")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_rc.tif'),"rc")
            calculo(' hm@1 - hbc@1 ',"lc")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_lc.tif'),"lc")
          
            #genero una carpeta para los datos intermedios            
            carpetap=os.path.join(carpeta,"p")
            carpeta=carpetap
            if not os.path.exists(carpetap):
                os.mkdir(carpetap)
            #proyecto la altura con el crecimiento
            calculo('(hm@1 < 5) * hm@1 + (hm@1 >= 5) * (hm@1 + ' +str(crecimiento)+')', 'hmp')
            StringToRaster(os.path.join(carpeta,troncoresumido+'_hmp.tif'),"hmp")
            #proyecto la altura  de la base de la copa con el crecimiento
            calculo('(hm@1 < 7.5) * hbc@1 + (hm@1 >= 7.5) * (hbc@1 + ' +str(crecimiento)+')','hbcp')
            StringToRaster(os.path.join(carpeta,troncoresumido+'_hbcp.tif'),"hbcp")
            #calculo  la razon de copa una vez proyectada la altura y la base de la copa
            calculo('100 * ( hmp@1   -  hbcp@1  ) / ( hmp@1 )', 'rcp')
            StringToRaster(os.path.join(carpeta,troncoresumido+'_rcp.tif'),"rcp")
            #proyecto la fraccion de cabida cubierta
            calculo('('+str(crecimiento)+' > 0) * (fcc@1  + ' +str(crecimientofcc)+') + ( '+str(crecimiento)+' = 0) * (fcc@1 )', 'fccp')
            StringToRaster(os.path.join(carpeta,troncoresumido+'_fccp.tif'),"fccp")
            #proyecto la longitud de copa
            calculo('(hmp@1 - hbcp@1)','lcp')
            StringToRaster(os.path.join(carpeta,troncoresumido+'_lcp.tif'),"lcp")

            #introduzco los condicionantes para cada tipo de masa
            calculo('(fccp@1 <= '+str(fccbaja)+') * 1 ','C1')
            calculo('(fccp@1 > '+str(fccbaja)+')*(hmp@1 < '+str(hmontebravoe)+')*2','C2')
            calculo('(fccp@1 >= '+str(fccmedia)+')*(hmp@1 >= '+str(hmontebravoe)+')*(hmp@1 < '+str(hmontebravo)+')*(rcp@1 <= '+str(rcclaras)+')*51','C3')
            calculo('(fccp@1 > '+str(fccbaja)+')*(hmp@1 >= '+str(hmontebravoe)+')*(hmp@1 < '+str(hmontebravo)+')*(rcp@1 <= '+str(rcclaras)+')*(fccp@1 < '+str(fccmedia)+')*61','C4')
            calculo('(fccp@1 > '+str(fccbaja)+')*(hmp@1 >= '+str(hmontebravoe)+')*(hmp@1 < '+str(hmontebravo)+')*(rcp@1 > '+str(rcclaras)+')*17', 'C5')
            calculo('(fccp@1 >= '+str(fccalta)+')*(hmp@1 >= '+str(hmontebravo)+')*(hmp@1 <= '+str(hselvicolas)+')*(rcp@1 <= '+str(rcclaras)+')*52', 'C8')
            calculo('(fccp@1 > '+str(fccbaja)+')*(hmp@1 >= '+str(hmontebravo)+')*(hmp@1 <= '+str(hselvicolas)+')*(rcp@1 <= '+str(rcclaras)+')*(fccp@1 < '+str(fccalta)+')*62', 'C9')
            calculo('(fccp@1 > '+str(fccbaja)+')*(hmp@1 >= '+str(hmontebravo)+')*(hmp@1 <= '+str(hselvicolas)+')*(rcp@1 > '+str(rcclaras)+')*(hbcp@1 <= '+str(hbcminima)+')*3', 'C6') 
            calculo('(fccp@1 > '+str(fccbaja)+')*(hmp@1 >= '+str(hmontebravo)+')*(hmp@1 <= '+str(hselvicolas)+')*(rcp@1 > '+str(rcclaras)+')*(hbcp@1 > '+str(hbcminima)+')*4','C7')
            calculo('(fccp@1 > '+str(fccbaja)+')*(hmp@1 > '+str(hselvicolas)+')*(hmp@1 <= '+str(hclaras)+')*(hbcp@1 <= '+str(hbcdesarrollado)+')*7', 'C10')
            #formula terrazas
            formula='(0.1167 * fccp@1 + 3.6667 ) * hmp@1 ^ 1.04328809 * ( hmp@1 - hbcp@1) ^ (-0.49505946)'
            calculo('(fccp@1 > '+str(fccterrazas)+')*(hmp@1 > '+str(hselvicolas)+')*(hmp@1 <= '+str(hclaras)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 >= '+str(rcclaras)+')*(lcp@1 > '+str(longitudcopaminima)+')*(fccp@1 >= '+str(formula)+')*81', 'C11')
            calculo('(fccp@1 > '+str(fccbaja)+')*(hmp@1 > '+str(hselvicolas)+')*(hmp@1 <= '+str(hclaras)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 >= '+str(rcclaras)+')*(lcp@1 <= '+str(longitudcopaminima)+')*7', 'C12')
            calculo('(fccp@1 > '+str(fccbaja)+')*(hmp@1 > '+str(hselvicolas)+')*(hmp@1 <= '+str(hclaras)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 >= '+str(rcclaras)+')*(lcp@1 > '+str(longitudcopaminima)+')*(fccp@1 <= '+str(fccterrazas)+')*7', 'C13')
            calculo('(fccp@1 >= '+str(fccalta)+')*(hmp@1 > '+str(hselvicolas)+')*(hmp@1 <= '+str(hclaras)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 >= '+str(rcclaras)+')*(lcp@1 > '+str(longitudcopaminima)+')*(fccp@1 < '+ str(formula)  +')*81', 'C15')
            calculo('(fccp@1 >= '+str(fccterrazas)+')*(hmp@1 > '+str(hselvicolas)+')*(hmp@1 <= '+str(hclaras)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 >= '+str(rcclaras)+')*(lcp@1 > '+str(longitudcopaminima)+')*(fccp@1 < '+ str(formula) +')*(fccp@1 < '+str(fccalta)+')*10', 'C16')
            calculo('(fccp@1 >= '+str(fccalta)+')*(hmp@1 > '+str(hselvicolas)+')*(hmp@1 <= '+str(hclaras)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 < '+str(rcclaras)+')*9','C14')    
            calculo('(fccp@1 > 20)*(fccp@1 < '+str(fccalta)+')*(hmp@1 > '+str(hselvicolas)+')*(hmp@1 <= '+str(hclaras)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 < '+str(rcclaras)+')*10', 'C17')
            calculo('(fccp@1 > 20)*(hmp@1 > '+str(hclaras)+')*(hmp@1 <= '+str(hclaras2)+')*(hbcp@1 <= '+str(hbcdesarrollado)+')*111', 'C18')
            calculo('(fccp@1 >= '+str(fccterrazas)+')*(hmp@1 > '+str(hclaras)+')*(hmp@1 <= '+str(hclaras2)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 >= '+str(rcclaras)+')*(lcp@1 > '+str(longitudcopaminima)+')*(fccp@1 > '+ str(formula)  +')*82', 'C19')
            calculo('(fccp@1 >= 20)*(hmp@1 > '+str(hclaras)+')*(hmp@1 <= '+str(hclaras2)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 >= '+str(rcclaras)+')*(lcp@1 <= '+str(longitudcopaminima)+')*111', 'C30')   
            calculo('(fccp@1 >= 20)*(hmp@1 > '+str(hclaras)+')*(hmp@1 <= '+str(hclaras2)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 >= '+str(rcclaras)+')*(lcp@1 > '+str(longitudcopaminima)+')*(fccp@1 <='+str(fccterrazas)+')*111', 'C29')
            calculo('(fccp@1 >= '+str(fccalta)+')*(hmp@1 > '+str(hclaras)+')*(hmp@1 <= '+str(hclaras2)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 >= '+str(rcclaras)+')*(lcp@1 > '+str(longitudcopaminima)+')*(fccp@1 < '+ str(formula)  +')*82', 'C21')
            calculo('(fccp@1 > '+str(fccterrazas)+')*(hmp@1 > '+str(hclaras)+')*(hmp@1 <= '+str(hclaras2)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 >= '+str(rcclaras)+')*(lcp@1 > '+str(longitudcopaminima)+')*(fccp@1 < '+str(fccalta)+')*(fccp@1 < '+ str(formula) +')*111', 'C22')             
            calculo('(fccp@1 >= '+str(fccalta)+')*(hmp@1 > '+str(hclaras)+')*(hmp@1 <= '+str(hclaras2)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 < '+str(rcclaras)+')*121','C20') 
            calculo('(fccp@1 > '+str(fccbaja)+')*(fccp@1 < '+str(fccalta)+')*(hmp@1 > '+str(hclaras)+')*(hmp@1 <= '+str(hclaras2)+')*(hbcp@1 > '+str(hbcdesarrollado)+')*(rcp@1 < '+str(rcclaras)+')*141', 'C23')
            calculo('(fccp@1 >= '+str(fccalta)+')*(hmp@1 > '+str(hclaras2)+')*(rcp@1 <= '+str(rcextremo)+')*13', 'C26')                       
            calculo('(fccp@1 < '+str(fccalta)+')*(fccp@1 > '+str(fccbaja)+')*(hmp@1 > '+str(hclaras2)+')*(rcp@1 <= '+str(rcextremo)+')*15', 'C28')
            calculo('(fccp@1 >= '+str(fccalta)+')*(hmp@1 > '+str(hclaras2)+')*(rcp@1 > '+str(rcextremo)+')*(rcp@1 < '+str(rcclaras)+')*122', 'C25')                      
            calculo('(fccp@1 < '+str(fccalta)+')*(fccp@1 > '+str(fccbaja)+')*(hmp@1 > '+str(hclaras2)+')*(rcp@1 > '+str(rcextremo)+')*(rcp@1 < '+str(rcclaras)+')*142', 'C27')
            calculo('(fccp@1 > '+str(fccbaja)+')*(hmp@1 > '+str(hclaras2)+')*(rcp@1 >= '+str(rcclaras)+')*112', 'C24')
              
            #empiezo carga de capas c
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C1.tif'),"c1")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C2.tif'),"c2")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C3.tif'),"c3")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C4.tif'),"c4")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C5.tif'),"c5")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C6.tif'),"c6")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C7.tif'),"c7")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C8.tif'),"c8")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C9.tif'),"c9")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C10.tif'),"c10")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C11.tif'),"c11")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C12.tif'),"c12")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C13.tif'),"c13")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C14.tif'),"c14")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C15.tif'),"c15")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C16.tif'),"c16")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C17.tif'),"c17")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C18.tif'),"c18")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C19.tif'),"c19")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C20.tif'),"c20")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C21.tif'),"c21")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C22.tif'),"c22")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C23.tif'),"c23")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C24.tif'),"c24")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C25.tif'),"c25")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C26.tif'),"c26")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C27.tif'),"c27")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C28.tif'),"c28")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C29.tif'),"c29")
            StringToRaster(os.path.join(carpeta,troncoresumido+'_C30.tif'),"c30")      
            #sumo todas las capas c
            calculo('c1@1 + c2@1 + c3@1 + c4@1 + c5@1 + c6@1 + c7@1 + c8@1+ c9@1+ c10@1+ c11@1 + c12@1 + c13@1 + c14@1 + c15@1 + c16@1 + c17@1 + c18@1 + c19@1 + c20@1 + c21@1 + c22@1+ c23@1 + c24@1 + c25@1 + c26@1 + c27@1 + c28@1+ c29@1 + c30@1', 'suma')
            StringToRaster(os.path.join(carpeta,troncoresumido+'_suma.tif'),"suma")
            #lo vectorizo
            processing.runalg("gdalogr:polygonize",os.path.join(carpeta,troncoresumido+'_suma.tif'),"DN",os.path.join(carpeta,troncoresumido+'_suma.shp'))
            sumashp=QgsVectorLayer(os.path.join(carpeta,troncoresumido+'_suma.shp'),"sumashp","ogr")
            QgsMapLayerRegistry.instance().addMapLayer(sumashp)
 
            #filtro para quedarme con la clara
            calculo('c11@1 / 8 + c14@1 / 9  + c15@1 / 8 + c19@1 / 8 + c20@1 / 12 + c21@1 / 8 + c25@1 / 12 + c26@1 / 13', 'clara1')
            StringToRaster(os.path.join(carpeta,troncoresumido+'_clara1.tif'),"clara1")
            agregado("clara")

            #filtro para quedarme con la regeneracion
            calculo('c28@1 / 15 ','regeneracion1')
            StringToRaster(os.path.join(carpeta,troncoresumido+'_regeneracion1.tif'),"regeneracion1")
            agregado("regeneracion")

            #filtro para quedarme con el resalveo
            calculo('c3@1 / 5 + c8@1 / 5', 'resalveo1')
            StringToRaster(os.path.join(carpeta,troncoresumido+'_resalveo1.tif'),"resalveo1")
            agregado("resalveo")
           
            #elimino las capas que he cargado durante el proceso
            capas =QgsMapLayerRegistry.instance().mapLayers()
            for capa in capas:
                if capa not in capasoriginales:
                    QgsMapLayerRegistry.instance().removeMapLayers( [capa] )
            break
    except:
        pass
#ejecuta la funcion que busca los archivos las y laz y a suvez ejecuta la funcion exprimelidar que hace el analisis de la cuadricula
buscalidaryejecuta(carpeta, crecimiento, fccbaja, fccterrazas, fccmedia, fccalta, hmontebravoe, hmontebravo, hselvicolas, hclaras, hclaras2, hbcminima, hbcdesarrollado, rcclaras, rcextremo, longitudcopaminima, crecimientofcc)

#defino una funcion que une en una capa el resultado de todas las hojas
def juntoshapes(busca,salida):
    files=glob.glob(busca)
    out=os.path.join(carpeta,salida+".shp")
    entrada=";".join(files)
    if len(files)>100:
        lista1=files[:len(files)/2]
        lista2=files[len(files)/2:]
        out=os.path.join(carpeta,salida+"1.shp")
        entrada=";".join(lista1)
        processing.runalg('saga:mergelayers',entrada,True,True,out)
        out=os.path.join(carpeta,salida+"2.shp")
        entrada=";".join(lista2)
        processing.runalg('saga:mergelayers',entrada,True,True,out)
    elif len(files) >1 and len(files) <=100:
        processing.runalg('saga:mergelayers',entrada,True,True,out)
    elif len(files) ==1:
        processing.runalg("qgis:saveselectedfeatures",files[0],out)
    else:
        pass
    del(out)
    del(entrada)
    del(files)
    
#uno en una capa todas las hojas de claras, regeneracion, resalveo y teselas
juntoshapes(os.path.join(carpeta,"p","*clara3.shp"),"Clara_merged")
juntoshapes(os.path.join(carpeta,"p","*regeneracion3.shp"),"Regeneracion_merged")
juntoshapes(os.path.join(carpeta,"p","*resalveo3.shp"),"Resalveo_merged")
juntoshapes(os.path.join(carpeta,"p","*suma.shp"),"Teselas_merged")

#elimino las capas que he cargado durante el proceso
capas =QgsMapLayerRegistry.instance().mapLayers()
for capa in capas:
    if capa not in capasoriginales:
        QgsMapLayerRegistry.instance().removeMapLayers( [capa] )
del(capas)
        
#cargo las capas finales
teselas=QgsVectorLayer(os.path.join(carpeta,'Teselas_merged.shp'),"Teselas","ogr")
teselas1=QgsVectorLayer(os.path.join(carpeta,'Teselas_merged_proyectado1.shp'),"Teselas Proyectado1","ogr")
teselas2=QgsVectorLayer(os.path.join(carpeta,'Teselas_merged_proyectado2.shp'),"Teselas Proyectado2","ogr")
clara=QgsVectorLayer(os.path.join(carpeta,'Clara_merged.shp'),"Clara","ogr")
regeneracion=QgsVectorLayer(os.path.join(carpeta,'Regeneracion_merged.shp'),"Regeneracion","ogr")
resalveo=QgsVectorLayer(os.path.join(carpeta,'Resalveo_merged.shp'),"Resalveo","ogr")

#aplico simbologia a estas capas, si existen
try:
    symbolsclara=clara.rendererV2().symbols()
    sym=symbolsclara[0]
    sym.setColor(QColor.fromRgb(255,0,0))
    QgsMapLayerRegistry.instance().addMapLayer(clara)
except: 
  pass

try:
    symbolsregeneracion=regeneracion.rendererV2().symbols()
    sym=symbolsregeneracion[0]
    sym.setColor(QColor.fromRgb(0,255,0))
    QgsMapLayerRegistry.instance().addMapLayer(regeneracion)
except: 
  pass

try:
    symbolsresalveo=resalveo.rendererV2().symbols()
    sym=symbolsresalveo[0]
    sym.setColor(QColor.fromRgb(0,0,255))
    QgsMapLayerRegistry.instance().addMapLayer(resalveo)
except: 
  pass

coloresteselas={"1":("solid","255,255,204,255","Raso o Regenerado","001"),"2":("solid","255,255,0,255","Menor (Monte Bravo)","002"),"3":("vertical","255,192,0,255","Poda Baja (y Clareo) en Bajo Latizal (Posibilidad si C elevada)","004"),"4":("solid","255,204,153,255","Bajo Latizal Desarrollado","005"),"51":("b_diagonal","255,0,255,255","Resalveo en Latizal poco desarrollado","006"),"52":("f_diagonal","255,0,0,255","Resalveo en Latizal","007"),"61":("solid","255,153,255,255","Latizal poco desarrollado Tratado","008"),"62":("solid","255,124,128,255","Latizal Tratado","009"),"7":("solid","204,255,153,255","Alto Latizal Claro","010"),"81":("b_diagonal","146,208,80,255","Poda Alta y Clara Suave en Latizal","011"),"82":("b_diagonal","51,204,204,255","Poda Alta y Clara Suave en Monte Desarrollado","015"),"9":("f_diagonal","0,176,80,255","Primera Clara y Poda Alta","012"),"10":("solid","102,255,153,255","Alto Latizal Aclarado","013"),"111":("solid","102,255,255,255","Fustal Claro","014"),"112":("solid","139,139,232,255","Fustal Maduro Claro","018"),"121":("f_diagonal","0,176,255,240","Clara en Fustal","016"),"122":("b_diagonal","65,51,162,255","Clara en Fustal Maduro","019"),"13":("cross","0,112,192,255","Clara Urgente en Fustal Maduro","020"),"141":("solid","204,236,255,255","Fustal Aclarado","017"),"142":("solid","166,166,207,255","Fustal Maduro Aclarado","021"),"15":("horizontal","112,48,160,255","Posibilidad de Regeneracion","022"),"17":("solid","orange","Bajo Latizal No Concurrente o Latizal Encinar no Denso","003")}

#ordeno los elementos de teselas
ordenados=coloresteselas.items()
ordenados.sort(key=lambda clave: str(clave[1][3]))

categorias=[]

for clase,(relleno,color, etiqueta,orden) in ordenados:    
    props={'style':relleno, 'color':color, 'style_border':'no'}
    sym=QgsFillSymbolV2.createSimple(props)
    categoria=QgsRendererCategoryV2(clase,sym,etiqueta)
    categorias.append(categoria)

field="DN"
renderer=QgsCategorizedSymbolRendererV2(field,categorias)
teselas.setRendererV2(renderer)
QgsMapLayerRegistry.instance().addMapLayer(teselas)

categorias1=[]
for clase,(relleno,color, etiqueta,orden) in ordenados:    
    props={'style':relleno, 'color':color, 'style_border':'no'}
    sym=QgsFillSymbolV2.createSimple(props)
    categoria1=QgsRendererCategoryV2(clase,sym,etiqueta)
    categorias1.append(categoria1)

field="DN"
renderer=QgsCategorizedSymbolRendererV2(field,categorias1)
teselas1.setRendererV2(renderer)
QgsMapLayerRegistry.instance().addMapLayer(teselas1)

categorias2=[]
for clase,(relleno,color, etiqueta,orden) in ordenados:    
    props={'style':relleno, 'color':color, 'style_border':'no'}
    sym=QgsFillSymbolV2.createSimple(props)
    categoria2=QgsRendererCategoryV2(clase,sym,etiqueta)
    categorias2.append(categoria2)

field="DN"
renderer=QgsCategorizedSymbolRendererV2(field,categorias2)
teselas2.setRendererV2(renderer)
QgsMapLayerRegistry.instance().addMapLayer(teselas2)

#repinto todo refrescando la vista
canvas.freeze(False)
canvas.refresh()

