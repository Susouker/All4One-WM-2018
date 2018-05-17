from math import *
import webcolors


def createPolygons(wheelW, wheelH):
    global center
    global coords
    global p,t
    center = [] #centers of the 4 wheels
    coords = [] #coords of the 4 wheel rectangles
    p = [] #polygon objects
    t = []
    
    wheelW /= 2
    wheelH /= 2
    origin = (w/2, h/2)
    
    for i in range (0,4):
        x = 1
        y = 1
        if(i % 2) == 1:
            x = -1
        if (i < 2):
            y = -1
        ce = (origin[0]+ x*_w/2, origin[1]+y*_wb/2)
        center.append(ce)
        
        xy = [(ce[0]-wheelW, ce[1]-wheelH), (ce[0]+wheelW, ce[1]-wheelH), (ce[0]+wheelW, ce[1]+wheelH), (ce[0]-wheelW, ce[1]+wheelH)]
        coords.append(xy)
        
        p.append(c.create_polygon(coords[i]))
        t.append(c.create_text(ce[0], ce[1]+wheelH+10, text='0', fill='white'))
    t.append(c.create_text(w/2, 10, text='0', fill='white'))


def update(r, msg):
    ret = []
    for i in range(0, 4):
        a = radians(r[0][i])
        ret.append(complex(cos(a), sin(a)))
        c.itemconfig(t[i], text="%d, %04.2f" %(r[0][i], r[1][i]))
        
        value = floor(abs(r[1][i]) * 256)
        c.itemconfig(p[i], fill=getHex(value))
        
    c.itemconfig(t[4], text=msg)
    rotatePolygons(ret)
    

def rotatePolygons(angles):
    for i in range(0, 4):
        offset = complex(center[i][0], center[i][1])
        newxy = []
        for x, y in coords[i]:
            v = angles[i] * (complex(x, y) - offset) + offset
            newxy.append(v.real)
            newxy.append(v.imag)
        c.coords(p[i], *newxy)
        
        
def setup(width, wheelbase, canvas, cW, cH, scale):
    global _w, _wb, c, w, h, scl
    scl = scale
    _w = width * scl
    _wb = wheelbase * scl
    c = canvas
    w = cW
    h = cH
    
    createPolygons(.05 * scl, .1 * scl)
    
    
def getHex(value):
        return webcolors.rgb_to_hex((value, value, value))