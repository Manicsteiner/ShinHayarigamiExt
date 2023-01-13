import os,sys,struct

from PIL import Image

def main():
    if not os.path.exists("graphics_bg.dat"):
        print("File not exist")
        return
    data = open("graphics_bg.dat", 'rb')
    os.system("mkdir graphics_bg")
    data.seek(6,0)
    filetotal = struct.unpack(">H",data.read(2))[0]
    print("Totaly " + str(filetotal) + " files")
    filestart = 0x55A
    
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
        nmt2png(picdata, filename)
        print("complete graphics_bg " + str(i+1))
    data.close()
    print("Complete!")

def getFileName(s):
    p = "{}s".format(len(s))
    s = struct.unpack(p,s)[0]
    rstr1 = str(s.replace(b"\x00",b"!"),encoding = "sjis",errors = "ignore")
    rstr2 = rstr1.rsplit('!', -1)[0]
    return rstr2

def nmt2png(picdata, filename):
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
    img.save("graphics_bg/" + filename + '.png', 'png')

def nmt2png_D(picdata, filename):
    filename = getFileNameWithoutExtension(filename)
    #width, height = 1280, 720
    width, height = struct.unpack("<2H",picdata[0x26:0x2a])
    #print(width)
    picraw = picdata[0x30:-0x20]
    img = Image.frombytes('RGBA',(width,height),picraw)
    img.save("graphics_bg/" + filename + '.png', 'png')

def getFileNameWithoutExtension(path):
    return path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

if __name__ =="__main__":
    main()
