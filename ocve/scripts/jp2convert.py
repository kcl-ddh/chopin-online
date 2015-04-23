#!/usr/bin/python
__author__ = 'Elliot'
import os

#If NOT exists /x/y/z/.somefile THEN
#touch /x/y/z/.somefile
#goto NEXTFILE
#Endif
#
#If mtime(/x/z/y/somefile) == mtime(/x/y/z/) THEN
#Process /x/y/z/somefile
#DEL /x/y/z/somefile
#DEL /x/y/z/.somefile
#Goto NEXTFILE
#Endif
#
#(else)
#touch /x/z/y/.somefile
#NEXTFILE

NEWJP2_UPLOAD_PATH = 'C:/Users/Elliot/Documents/projects/ocve2/media/temp'
CONVERTED_UPLOAD_PATH='/vol/ocve2/images/temp'
TIF_UPLOAD_PATH='/vol/ocve2/images/upload'
#f='4940.tif'

def parseFolder(folder):
    files=os.listdir(folder)
    for f in files:
        parseFile(folder,f)

def parseFile(folder,f):
    if str(f).find('.') > 0 and str(f).find('.tif') > 0:
            if os.path.isfile(folder+'/.'+f) is False:
                #Create new temp file
                os.system('touch '+folder+'/.'+f)
                tempfile = open(folder+'/.'+f,'w')
                tempfile.write(str(os.stat(folder+'/'+f).st_size))
                tempfile.close()
            else:
                tempfile = open(folder+'/.'+f,'r')
                size=tempfile.readline().replace('\n','')
                tempfile.close()
                print size
                if int(os.stat(folder+'/'+f).st_size) == int(size):
                    #File finished, convert
                    #Make new folder if necessary
                    #kdu_compress -i /vol/ocve2/images/jp2/ocvejp2-proc/20/3/02/20-1-W_USCu_p02.tif -o /vol/ocve2/images/jp2/ocvejp2-proc/20/3/02/20-1-W_USCu_p02.jp2 -rate -,4,2.34,1.36,0.797,0.466,0.272,0.159,0.0929,0.0543,0.0317,0.0185 Creversible=yes Clevels=5 Stiles=\{1024,1024\} Cblk=\{64,64\} Corder=RPCL Cmodes=BYPASS

                    dir=str(folder).split('/')
                    index=len(dir)
                    index-=1
                    if os.path.isdir(CONVERTED_UPLOAD_PATH+'/'+dir[index]) is False:
                        print 'mkdir '+CONVERTED_UPLOAD_PATH+'/'+dir[index]
                        os.system('mkdir "'+CONVERTED_UPLOAD_PATH+'/'+dir[index]+'"')
                    kdu_options='-rate -,4,2.34,1.36,0.797,0.466,0.272,0.159,0.0929,0.0543,0.0317,0.0185 Creversible=yes Clevels=5 Stiles=\{1024,1024\} Cblk=\{64,64\} Corder=RPCL Cmodes=BYPASS'
                    kdu_command='kdu_compress -i "'+folder+'/'+f+'" -o "'+CONVERTED_UPLOAD_PATH+'/'+dir[index]+'/'+str(f).split('.')[0]+'.jp2" '+kdu_options
                    os.system(kdu_command)
                    #Delete temp
                    os.system('rm '+folder+'/.'+f)
                else:
                    #Refresh temp
                    tempfile = open(folder+'/.'+f,'w')
                    tempfile.write(str(os.stat(folder+'/'+f).st_size))
                    tempfile.close()

def main():
    files=os.listdir(TIF_UPLOAD_PATH)
    for f in files:
        if os.path.isdir(TIF_UPLOAD_PATH+'/'+f) is True:
            parseFolder(TIF_UPLOAD_PATH+'/'+f)
        elif os.path.isdir(TIF_UPLOAD_PATH+'/'+f) is False:
            parseFile(TIF_UPLOAD_PATH,f)


if __name__ == "__main__":
    main()