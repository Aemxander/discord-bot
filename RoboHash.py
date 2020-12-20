import os
import random
import string
import sys

from robohash import Robohash


# get robot image from robohash
def GetRobot(hash=None, set='set1', background=None):
    # if no hash is passed in
    if hash == None:
        length = 20
        letters = string.ascii_lowercase
        hash = ''.join(random.choice(letters) for i in range(length))

    # create Robohash object
    rh = Robohash(hash)

    # assemble robot from parameters
    rh.assemble(roboset=set, bgset=background, sizex=500, sizey=500)

    # open/create image
    with open(os.path.join(sys.path[0], 'Robot.png'), 'wb') as f:
        # save robot image
        rh.img.save(f, format="png")

    #create robot message
    if set == 'set1':
        robotMessage = "**beep boop**"
    if set == 'set2':
        robotMessage = "**aarooo**"
    if set == 'set3':
        robotMessage = "**beep boop**"
    if set == 'set4':
        robotMessage = "**meow**"
    if set == 'set5':
        robotMessage = "**ayaya**"



    # return filename
    return 'Robot.png', robotMessage
