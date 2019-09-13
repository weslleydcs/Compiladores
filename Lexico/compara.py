import os

for i in range(0, 5000):
    print(str(i).zfill(4))
    os.system("diff saidas/t"+str(i).zfill(4)+" minhas_saidas/r"+str(i).zfill(4)+" > diff/diff"+str(i).zfill(4))
os.system("find ./diff -empty -delete")
