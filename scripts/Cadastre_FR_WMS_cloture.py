##Cadastre FR=group
##Cadastre FR - WMS - Cloture=name

##Couche_commune=vector
##Champ_code_INSEE=field Couche_commune
##Champ_nom_de_commune=field Couche_commune
##Code_EPSG=string 2154

from qgis.core import QgsRasterLayer,QgsMapLayerRegistry
from qgis.utils import iface,QgsMessageBar

layer = processing.getObject(Couche_commune)

if Code_EPSG == '2154' or Code_EPSG == '3942' or Code_EPSG == '3943' or Code_EPSG == '3944' or Code_EPSG == '3945' or Code_EPSG == '3946' or Code_EPSG == '3947' or Code_EPSG == '3948' or Code_EPSG == '3949' or Code_EPSG == '3950' or Code_EPSG == '32630' or Code_EPSG == ' 32631' or Code_EPSG == '32632' or Code_EPSG == '3857' or Code_EPSG == '4326' or Code_EPSG == '4258' or Code_EPSG == '32620' or Code_EPSG == '2970' or Code_EPSG == '2972' or Code_EPSG == '2973' or Code_EPSG == '2975' or Code_EPSG == '32622' or Code_EPSG == '32740' or Code_EPSG == '32738' or Code_EPSG == '4471' or Code_EPSG == '32621' :
    progress.setText(u'Systeme de coordonnees - EPSG : ' + Code_EPSG)

    tab = []

    for f in layer.getFeatures():

        col_select =str(f[Champ_code_INSEE]),f[Champ_nom_de_commune]
        tab.append(col_select)

        #Permet la suppression des doublons
        Lt= list(set(tab))
        Lt.sort()

    for c_insee, n_couche in Lt  :

        #AMORCES_CAD,LIEUDIT,CP.CadastralParcel,SUBFISCAL,CLOTURE,DETAIL_TOPO,HYDRO,VOIE_COMMUNICATION,BU.Building,BORNE_REPERE
        urlWithParams = "url=http://inspire.cadastre.gouv.fr/scpc/"+c_insee+".wms?contextualWMSLegend=0&crs=EPSG:"+Code_EPSG+"&dpiMode=7&featureCount=10&format=image/png&layers=CLOTURE&styles="

        rlayer = QgsRasterLayer(urlWithParams, 'Cloture_'+n_couche+'_'+c_insee, 'wms')

        progress.setText(u'Nom de la commune : ' + n_couche+' - '+c_insee)
        progress.setText(u'Validite du flux : %s' % rlayer.isValid())

        QgsMapLayerRegistry.instance().addMapLayer(rlayer)

        if  rlayer.isValid() == True :
            iface.messageBar().pushMessage("Information :", "Ajout du flux WMS pour la commune : "+n_couche, QgsMessageBar.INFO, duration=5)
            iface.mapCanvas().refresh()

        else :
            iface.messageBar().pushMessage("Warning :", "WMS invalide pour la commune : "+n_couche, QgsMessageBar.WARNING, duration=15)

else :
    iface.messageBar().pushMessage("Warning :", "EPSG inconnu", QgsMessageBar.WARNING, duration=15)
    progress.setText(u'EPSG inconnu')
