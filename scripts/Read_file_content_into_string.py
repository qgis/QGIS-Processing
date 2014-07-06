##Utils=group
##Read file content into string=name
##Source_file=file
##output=output string

import os

string = ""
# Read only the first 10Mb of the file
with open(Source_file, 'r') as f:
    string = f.read(10485760)

progress.setInfo('<b>First 1000 characters of the output string: </b></br>%s' % string[:1000])

output = string