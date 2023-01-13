import os,sys,struct

from PIL import Image

def getFileNameWithoutExtension(path):
    return path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

def nmt2png(file):
    fl = open(file, 'rb')
    filename = getFileNameWithoutExtension(file)
    #fl.seek(16,0)
    #filestart = struct.unpack(">I",fl.read(4))[0]
    fl.seek(0x26,0)
    width, height = struct.unpack("<2H",fl.read(4))
    #width, height = 1280, 720
    img = Image.new('RGBA', (width, height))
    fl.seek(0x30,0)
    for y in range(height):
        for x in range(width):
            color = fl.read(4)
            img.putpixel((x, y), (color[2], color[1], color[0], color[3]))
    fl.close()
    img.save(filename + '.png', 'png')
    print("nmt2png: '" + file + "' convert png success! Save as '" + filename + '.png' + "'")

if __name__ == '__main__':
    if len(sys.argv) < 2 :
        exit()
    files=[]
    files=sys.argv[1:]
    for file in files:
        gtf2png(file)
