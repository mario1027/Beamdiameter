from mayavi import mlab
import cv2
import numpy as np

cap=cv2.VideoCapture("output.mp4")
ret, img = cap.read()
height, width = img.shape

# A mesh grid
xs = np.linspace(0,width,width)
ys = np.linspace(0,height,height)
x,y = np.meshgrid(xs, ys)

z = img

obj = mlab.mesh(x,y,z, color= (1, 1, 1))

max_framerate = 10

ms = obj.mlab_source
@mlab.animate(delay=100)
def anim():
    while 1:
        retval, img = cap.read()


        a,b = 300,212
        size = 200
        img = img[b-size/2:b+size/2, a-size/2:a+size/2]

        ms.set(x=x, y=y, z=img)
        yield

        anim()
        mlab.show()