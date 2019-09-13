import os

for i in range(0, 5000):
    print(str(i).zfill(4))
    os.system("python programa.py < entradas/t"+str(i).zfill(4)+" > minhas_saidas/r"+str(i).zfill(4))
