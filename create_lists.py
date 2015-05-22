
import glob
import os
import json

if __name__ == '__main__':    
    scripts = []
    for filename in glob.glob('scripts/*.py'):
        print filename
        basename = os.path.basename(filename)
        name = basename[:-3].replace('_', ' ')
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                if line.endswith('name'):
                    name = line.split('=')[0][2:]
        helpFile = filename + ".help"
        if not os.path.exists(helpFile):
            version = 1
        else:
            with open(helpFile) as f:                
                try:
                    helpContent = json.load(f)
                    version = float(helpContent["ALG_VERSION"])
                except:
                    version = 1
        scripts.append('%s,%s,%s' % (basename, version, name))
    scripts = sorted( scripts )
    with open('scripts/list.txt', 'w') as f:
        f.write('\n'.join(scripts))
		


