import os,sys,struct

#from PIL import Image

def main():
    if not os.path.exists("sound_bgm.dat"):
        print("File not exist")
        return
    data = open("sound_bgm.dat", 'rb')
    os.system("mkdir sound_bgm")
    data.seek(6,0)
    filetotal = struct.unpack(">H",data.read(2))[0]
    print("Totaly " + str(filetotal) + " files")
    filestart = 0x118
    
    for i in range (filetotal):
        data.seek(filestart+i*23,0)
        fstart,flength = struct.unpack(">2I",data.read(8))
        #data.seek(flnamestart+namepl,0)
        filename = getFileName(b'' + data.read(12))
        wrfile = open("sound_bgm/"+filename, 'wb')
        data.seek(fstart)
        wrfile.write(data.read(flength))
        wrfile.close()
        print("complete sound " + str(i+1))
    data.close()
    print("Complete!")

def getFileName(s):
    p = "{}s".format(len(s))
    s = struct.unpack(p,s)[0]
    rstr1 = str(s.replace(b"\x00",b"!"),encoding = "sjis",errors = "ignore")
    rstr2 = rstr1.rsplit('!', -1)[0]
    return rstr2

if __name__ =="__main__":
    main()
