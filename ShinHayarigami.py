import os,sys,struct

from PIL import Image
import numpy as np

def main(file):
    if file == "graphics_bg.dat" or file == "graphics_ci.dat":
        dataprocessgraphic(file)
    else:
        dataprocess(file)

def dataprocessgraphic(file):
    if not os.path.exists(file):
        print("File not exist")
        return
    
    if file == "graphics_ci.dat":
        filestart = 4710
    elif file == "graphics_bg.dat":
        filestart = 0x55A
    else:
        print("Not recognized file")
        return
    
    data = open(file, 'rb')
    os.system("mkdir " + getFileNameWithoutExtension(file))
    data.seek(6,0)
    filetotal = struct.unpack(">H",data.read(2))[0]
    print("Totaly " + str(filetotal) + " files")
    
    for i in range (filetotal):
        data.seek(filestart+i*22,0)
        fstart,flength = struct.unpack(">2I",data.read(8))
        #data.seek(flnamestart+namepl,0)
        filename = getFileName(b'' + data.read(11))
        #wrfile = open("graphics_bg/"+filename, 'wb')
        data.seek(fstart)
        picdata = b'' + data.read(flength)
        #print(picdata[0x26])
        #wrfile.close()
        nmt2png(picdata, filename, file)
        print("complete " + getFileNameWithoutExtension(file) + " " + str(i+1))
    data.close()
    print("Complete!")
    
def dataprocess(file):
    if not os.path.exists(file):
        print("File not exist")
        return
    
    if file == "sound_bgm.dat":
        filestart = 0x118
    elif file == "sound_se.dat":
        filestart = 0x1A40
    elif file == "start.dat":
        filestart = 0x6EA
    elif file == "database.dat":
        filestart = 0x140
    else:
        print("Not recognized file")
        return
    
    data = open(file, 'rb')
    os.system("mkdir " + getFileNameWithoutExtension(file))
    data.seek(6,0)
    filetotal = struct.unpack(">H",data.read(2))[0]
    print("Totaly " + str(filetotal) + " files")
    
    for i in range (filetotal):
        data.seek(filestart,0)
        fstart,flength = struct.unpack(">2I",data.read(8))
        #data.seek(flnamestart+namepl,0)
        fnameb = []
        fnamelength = 0
        #fnamecont = True
        while True:
            tempbyte = b'' + data.read(1)
            if tempbyte == b"\x00":
                break
            fnameb.append(tempbyte)
            fnamelength += 1
        
        fnamelength += 11
        #filename = getFileName(b'' + data.read(12))
        filename = getFileName(np.array(fnameb, dtype = bytes))
        if filename.endswith(".nmt"):
            #handle the pic
            data.seek(fstart)
            picdata = b'' + data.read(flength)
            nmt2png(picdata, filename, file)
        else:
            wrfile = open(getFileNameWithoutExtension(file) + "/" + filename, 'wb')
            data.seek(fstart)
            wrfile.write(data.read(flength))
            wrfile.close()
        print("complete " + getFileNameWithoutExtension(file) + " " + str(i+1))
        filestart += fnamelength
        #print(filestart)
    data.close()
    print("Complete!")

def getFileName(s):
    p = "{}s".format(len(s))
    s = struct.unpack(p,s)[0]
    rstr1 = str(s.replace(b"\x00",b"!"),encoding = "sjis",errors = "ignore")
    rstr2 = rstr1.rsplit('!', -1)[0]
    return rstr2

def nmt2png(picdata, filename, datafile):
    #fl = open(file, 'rb')
    filename = getFileNameWithoutExtension(filename)
    #picdata.seek(0x26,0)
    #width, height = struct.unpack("<2H",picdata.read(4))
    width, height = struct.unpack("<2H",picdata[0x26:0x2a])
    #width, height = 1280, 720
    #width = int.from_bytes(picdata[0x26:0x27], 'little')
    #height = int.from_bytes(picdata[0x28:0x29], 'little')
    #print(str(width))
    img = Image.new('RGBA', (width, height))
    #fl.seek(0x30,0)
    p = 0x30
    for y in range(height):
        for x in range(width):
            #color = picdata.read(4)
            img.putpixel((x, y), (picdata[p+2], picdata[p+1], picdata[p], picdata[p+3]))
            p+=4
    #fl.close()
    img.save(getFileNameWithoutExtension(datafile) + "/" + filename + '.png', 'png')

def nmt2png_D(picdata, filename):
    filename = getFileNameWithoutExtension(filename)
    #width, height = 1280, 720
    width, height = struct.unpack("<2H",picdata[0x26:0x2a])
    #print(width)
    picraw = picdata[0x30:-0x20]
    img = Image.frombytes('RGBA',(width,height),picraw)
    img.save("graphics_ci/" + filename + '.png', 'png')

def getFileNameWithoutExtension(path):
    return path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

if __name__ =="__main__":
    if len(sys.argv) < 2 :
        exit()
    files=[]
    files=sys.argv[1:]
    for file in files:
        main(file)
