import os, random

def rndmp3():
    randomfile = random.choice(os.listdir("/home/kennethmikolaichik/Music/Classical/"))
    file = ' /home/kennethmikolaichik/Music/Classical/'+ randomfile
    os.system ('mplayer' + file)

rndmp3()

