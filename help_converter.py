import glob
import pickle
import json

for filename in glob.glob('scripts/*.help'):
	with open(filename, 'rb') as f:
		try: 
		    descriptions = pickle.load(f)
		    with open(filename, 'w') as f:
		        f.write(json.dumps(descriptions))
		except :
		    pass
