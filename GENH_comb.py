import os,sys,struct

def main(name):
    if not os.path.exists(name + ".genh") or not os.path.exists(name + ".lpcm"):
        print("File not exist")
        return
    file1 = open(name + ".genh", 'rb')
    file2 = open(name + ".lpcm", 'rb')
    data1 = b'' + file1.read()
    data2 = b'' + file2.read()
    headersize = os.path.getsize(name + ".genh")
    wrfile = open(name + ".combine.genh", 'wb')
    wrfile.write(data1)
    wrfile.write(data2[headersize:])
    wrfile.close()
    print("Complete!")

def cstr(s):
    p = "{}s".format(len(s))
    s = struct.unpack(p,s)[0]
    return str(s.replace(b"\x00",b""),encoding = "sjis")
    
if __name__ =="__main__":
    if len(sys.argv) < 2 :
        main("OP")
    files=[]
    files=sys.argv[1:]
    for name in files:
        main(name)
    
