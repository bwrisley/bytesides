#!/usr/bin/env python
import sys,re,os
from subprocess import call, check_call

def unbup(filepath,filename):
    b = bytearray(open(filepath, 'rb').read())
    for i in range(len(b)):
        b[i] ^= 0x6A
    open('temp/'+filename, 'wb').write(b)
    return True

if __name__ == "__main__":
    print 'bupcrave v0.2'

    try:
        check_call(["foremost", "-V"])
    except OSError:
        sys.exit('Foremost not found! Install it first.')

    if os.path.isdir(sys.argv[1]):
        for root, subFolders, files in os.walk(sys.argv[1]):
            for filename in files:
                if filename.split('.')[-1] == 'bup':
                    filePath = os.path.join(root,filename)
                    fileName = re.split('\.|/',filePath)[-2]
                    craveSrc = "temp/"+fileName
                    craveDst = "dump/"+fileName
                    unbup(filePath,fileName)
                    call(["foremost",craveSrc,"-o" + craveDst,"-v"])
