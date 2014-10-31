##Classification by decision tree=group
##Vector_samples=vector
##Classes_field=field Vector_samples
##Vector_datas=vector
##Maximum_depth=number 0
##Output_classification=output vector
#Import time
import time
#Import library to QGIS
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
#Import processing
from processing.core.VectorWriter import VectorWriter
from processing.core.GeoAlgorithmExecutionException import \
        GeoAlgorithmExecutionException
#import sklearn
try:

    from sklearn import tree
    from sklearn.feature_extraction import DictVectorizer
    vec = DictVectorizer()
    
except:
    raise GeoAlgorithmExecutionException("Scikit-Learn isn't insalled")

class ClassificationDecisionTree:
        
    def createSample(self):
        '''
        Input sample vector
        Create array from vector 
        Output training (list(dict)) and class (list)
        '''        
        #Open layer sample 
        layer_sample = processing.getObject(Vector_samples)
        #Get index fields
        idx_field_class = layer_sample.fieldNameIndex(Classes_field)
        #iniciar variaveis auxiliares
        self.classes=[]
        self.training=[]
        #Get names fields sample
        layer_features = layer_sample.getFeatures()
        fields = layer_sample.pendingFields()
        #Get names fields sample
        fields_names = [str(i.name()) for i in fields]
        #Remover field class
        fields_names.remove(Classes_field)
        #Loop about features sample
        for feat in layer_features:
            #Get values attibutes
            attributes = feat.attributes()
            #Remove values classes e add in variable
            v_class = attributes.pop(idx_field_class)
            #Append value class
            self.classes.append(v_class)
            #Create dict from attr
            atr = dict(zip(fields_names, attributes))
            #Append in training
            self.training.append(atr)
            
    def createDatas(self):
        '''
        Input datas vector
        Create array from vector 
        Output datas (list(dict))
        '''
        
        #Open layer datas
        self.layer_datas = processing.getObject(Vector_datas)

        #iniciar variaveis auxiliares
        self.datas=[]
        #Get names fields sample
        features_datas = self.layer_datas.getFeatures()
        #Get fields vector datas
        fields = self.layer_datas.pendingFields()
        #Get names fields sample
        fields_names = [str(i.name()) for i in fields]
        #Loop features datas vector
        for feat in features_datas:
            #create datas from dict
            atr = dict(zip(fields_names, feat.attributes()))
            self.datas.append(atr)
  
    def classifierTree(self,Max_depth):
        '''
        Create model tree 
        Input training (list(dicy)), class (list) and datas (list(dict))
        Output list with classification of Datas
        '''
    
        #Create fit transform
        trans_train = vec.fit_transform(self.training).toarray()
        del(self.training)
        trans_datas = vec.fit_transform(self.datas).toarray()
        
        #Choose type classification
        clf = tree.DecisionTreeClassifier( max_depth = Max_depth)
        #Crate model classification tree
        modelTree = clf.fit(trans_train, self.classes)
        print 'max_n_classes, ', modelTree.tree_.max_n_classes
        print 'node_count: ', modelTree.tree_.node_count
        print 'min_density: ', modelTree.tree_.min_density
        print 'n_outputs: ', modelTree.tree_.n_outputs
        print 'n_features: ', modelTree.tree_.n_features
        print 'n__classes: ', modelTree.tree_.n_classes
        print 'n_samples: ', modelTree.tree_.n_samples
    
        del(trans_train)
        del(self.classes)
        #Apply model classification in Datas
        self.classificationDatas = modelTree.predict(trans_datas)
        
        with open("/home/ruiz/tree.dot", 'w') as f:
            f = tree.export_graphviz(modelTree, out_file=f)
    def writeClassification(self):
        #Create vector to write
        provider = self.layer_datas.dataProvider()
        #fields
        fields = provider.fields()
        fields=[i for i in fields]
        fields.append(QgsField("class", QVariant.Int))
        #Create shape writer
        self.writer = VectorWriter(Output_classification, None, fields, provider.geometryType(), self.layer_datas.crs())
        for i, feat in enumerate(self.layer_datas.getFeatures()):
            #Add features write
            fet = QgsFeature()
            fet.setGeometry(feat.geometry())
            attrs=feat.attributes()
            attrs.append(int(self.classificationDatas[i]))
            fet.setAttributes(attrs)
            self.writer.addFeature(fet)     
        del(self.writer)
        
ini=time.time()
#Assess parameters tree
try:
           
            if Maximum_depth <= 0:
               Maximum_depth = None
            else:
                Maximum_depth  =int(Maximum_depth)
except:
            raise GeoAlgorithmExecutionException("Error parameters CART - use integer number")
#Create class
progress.setText("Init classification by decision tree (CART)")
progress.setPercentage(10)
func = ClassificationDecisionTree()
#create sample
progress.setText("Create samples")
progress.setPercentage(25)
func.createSample()
#Create func Dataset
progress.setText("Create datas")
progress.setPercentage(50)
func.createDatas()
#Create func to classifier decision tree
progress.setText("Create model CART")
progress.setPercentage(75)
func.classifierTree(Maximum_depth)
#Add classification in write
progress.setText("Write classification")
func.writeClassification()
progress.setPercentage(100)
fim = time.time()
temp =(fim-ini)/60
progress.setText("finish - Time in minutes: "+str(temp))
time.sleep(4)

print "Time in minutes: ", (fim-ini)/60
