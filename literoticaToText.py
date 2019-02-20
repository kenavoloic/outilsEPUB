import os

a = os.listdir('.')
for x in a:
    os.rename(x,x+'.txt')
