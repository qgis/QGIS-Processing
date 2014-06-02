import processing
import pickle
import json

for filename in glob.glob('D:/github/processing/scripts/*.help'):
	with open(filename, 'rb') as f:
		descriptions = pickle.load(f)
	with open(filename, 'w') as f:
		f.write(json.dumps(descriptions))