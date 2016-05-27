import glob
import pickle
import json

def convertHelp( filePath ):
    with open(filePath, 'rb') as f:
        try:
            descriptions = pickle.load(f)
            with open(filePath, 'w') as f:
                f.write(json.dumps(descriptions))
        except :
            pass

for filename in glob.glob('scripts/*.help'):
    convertHelp( filename )

for filename in glob.glob('rscripts/*.help'):
    convertHelp( filename )

for filename in glob.glob('models/*.help'):
    convertHelp( filename )
