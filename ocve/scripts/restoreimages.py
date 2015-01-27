__author__ = 'Elliot'
#A script to fix some images from OCVE 1 that weren't converted to jp2 properly
import os
import re
#from ocve.models import *




def main():
    kdu_options = '-rate -,4,2.34,1.36,0.797,0.466,0.272,0.159,0.0929,0.0543,0.0317,0.0185 Creversible=yes Clevels=5 Stiles=\{1024,1024\} Cblk=\{64,64\} Corder=RPCL Cmodes=BYPASS'
    images = open('zeros.txt', 'r')
    log = open('log.txt','w')
    for line in images:
        #./38/15/11/38-1-W_GBOb_p11.jp2
        f = re.match(r'^\.(\/.*)\/(.*)\.jp2', line)
        if f is not None:
            path=f.group(1)
            filename = f.group(2)
            if filename is not None:
                source = '/vol/iproc/ocve2/cfeotif' + path+'/'+ filename + '.tif'
                target = '/vol/ocve2/images/jp2/ocvejp2-proc'+ path+'/'+ filename + '.jp2'
                kdu_command = 'kdu_compress -i "' + source + '" -o "' + target + '" ' + kdu_options
                print kdu_command
                os.system(kdu_command)
                #Verify jp2 size is no longer zero
                size = os.path.getsize(target)
                if size == 0:
                    log.write(target+' still zero\n')
    images.close()
    log.close()


if __name__ == "__main__":
    main()