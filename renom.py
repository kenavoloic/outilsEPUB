import os

def traitement(chaine):
    t = os.listdir(".")
    print t
    for x in t:
        if x.startswith(chaine):
            os.rename(x,x[len(chaine):])
    print "Fini !"

if __name__ == '__main__':
    u = sys.argv
    traitement(u[1])
