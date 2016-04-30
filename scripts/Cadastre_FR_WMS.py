##Cadastre FR=group
##Cadastre FR - WMS - Add a cadastral map=name

##Vector_layer_of_communes=vector
##INSEE_code=field Vector_layer_of_communes
##Commune_name=field Vector_layer_of_communes
##EPSG_code=string 2154

from qgis.core import QgsRasterLayer,QgsMapLayerRegistry
from qgis.utils import iface,QgsMessageBar

layer = processing.getObject(Vector_layer_of_communes)

if EPSG_code == '2154' or EPSG_code == '3942' or EPSG_code == '3943' or EPSG_code == '3944' or EPSG_code == '3945' or EPSG_code == '3946' or EPSG_code == '3947' or EPSG_code == '3948' or EPSG_code == '3949' or EPSG_code == '3950' or EPSG_code == '32630' or EPSG_code == ' 32631' or EPSG_code == '32632' or EPSG_code == '3857' or EPSG_code == '4326' or EPSG_code == '4258' or EPSG_code == '32620' or EPSG_code == '2970' or EPSG_code == '2972' or EPSG_code == '2973' or EPSG_code == '2975' or EPSG_code == '32622' or EPSG_code == '32740' or EPSG_code == '32738' or EPSG_code == '4471' or EPSG_code == '32621' :
    progress.setText(u'EPSG code : ' + EPSG_code)

    tab = []

    for f in layer.getFeatures():

        col_select =str(f[INSEE_code]),f[Commune_name]
        tab.append(col_select)

        #Permet la suppression des doublons
        Lt= list(set(tab))
        Lt.sort()

    for c_insee, n_couche in Lt  :

        #AMORCES_CAD,LIEUDIT,CP.CadastralParcel,SUBFISCAL,CLOTURE,DETAIL_TOPO,HYDRO,VOIE_COMMUNICATION,BU.Building,BORNE_REPERE
        urlWithParams = "url=http://inspire.cadastre.gouv.fr/scpc/"+c_insee+".wms?contextualWMSLegend=0&crs=EPSG:"+EPSG_code+"&dpiMode=7&featureCount=10&format=image/png&layers=AMORCES_CAD&layers=LIEUDIT&layers=CP.CadastralParcel&layers=SUBFISCAL&layers=CLOTURE&layers=DETAIL_TOPO&layers=HYDRO&layers=VOIE_COMMUNICATION&layers=BU.Building&layers=BORNE_REPERE&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&maxHeight=1024&maxWidth=1280"

        rlayer = QgsRasterLayer(urlWithParams, 'Cadastre_'+n_couche+'_'+c_insee, 'wms')

        progress.setText(u'Commune name : ' + n_couche+' - '+c_insee)
        progress.setText(u'Validity of WMS : %s' % rlayer.isValid())

        QgsMapLayerRegistry.instance().addMapLayer(rlayer)

        if  rlayer.isValid() == True :
            iface.messageBar().pushMessage("Information :", "Adding a cadastral map : "+n_couche, QgsMessageBar.INFO, duration=5)
            iface.mapCanvas().refresh()

        else :
            iface.messageBar().pushMessage("Warning :", "WMS invalid : "+n_couche, QgsMessageBar.WARNING, duration=15)

else :
    iface.messageBar().pushMessage("Warning :", "EPSG is unknown ", QgsMessageBar.WARNING, duration=15)
    progress.setText(u'EPSG is unknown ')
