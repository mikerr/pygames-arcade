# 3dcube - wireframe, solid and shaded
import os, math, time
import pygame

screen = pygame.display.set_mode()

def rot3d (point,rotate) :
    x,y,z = point
    rx,ry,rz = rotate
            
    # about z axis 
    nX = (math.cos(rz) * x) - (math.sin(rz) * y)
    nY = (math.sin(rz) * x) + (math.cos(rz) * y)
    x = nX 
    y = nY

    # about x axis 
    nZ = (math.cos(rx) * z) - (math.sin(rx) * y)
    nY = (math.sin(rx) * z) + (math.cos(rx) * y)
    z = nZ

    # about y axis 
    nX = (math.cos(ry) * x) - (math.sin(ry) * z)
    nZ = (math.sin(ry) * x) + (math.cos(ry) * z)

    return ((nX,nY,nZ))
        
def normal (triangle) :
    t1,t2,t3 = triangle
    
    x1,y1,z1 = t1
    x2,y2,z2 = t2
    x3,y3,z3 = t3
    
    #A = t2 - t1
    A = (x2-x1, y2-y1, z2-z1)
    
    #B = t3 - t1
    B = (x3-x1, y3-y1, z3-z1)
    
    # A cross product B
    Ax,Ay,Az = A
    Bx,By,Bz = B
    
    Nx = Ay * Bz - Az * By
    Ny = Az * Bx - Ax * Bz
    Nz = Ax * By - Ay * Bx
    
    return ((Nx,Ny,Nz))

def dotproduct(A,B):
     ax,ay,az = A
     bx,by,bz = B
 
     return ( ax * bx + ay * by + az * bz)

def to2d(xyz):
    x,y,z = xyz
    z = z - 150
    x = x * 500  / z
    y = y * 500  / z
    return ((120 + int(x),120 + int(y)))

mode = angle = 2
facecolors= []
points = []
faces = []
def init() :
        global points, faces, facecolors 
        #cube points
        points = [
            [ 10,  10,  10],
             [-10,  10,  10],
             [-10, -10,  10],
             [ 10, -10,  10],
             [ 10,  10, -10],
             [-10,  10, -10],
             [-10, -10, -10],
             [ 10, -10, -10]]
        # cube faces
        # (triangles)
        faces = [
            [0, 1, 2],
            [0, 2, 3],
            [4, 0, 3],
            [4, 3, 7],
            [5, 4, 7],
            [5, 7, 6],
            [1, 5, 6],
            [1, 6, 2],
            [4, 5, 1],
            [4, 1, 0],
            [2, 6, 7],
            [2, 7, 3]]
        facecolors = [
            [255,0,0], # red
            [255,0,0],
            [0,255,0], # green
            [0,255,0],
            [0,0,255], # blue
            [0,0,255],
            [255,255,0], # yellow
            [255,255,0],
            [0,255,255], # cyan
            [0,255,255],
            [255,0,255], # magenta
            [255,0,255]
            ]
         
def update(tick) :
        global angle,mode
        angle += 0.1
        
def draw(tick) :
        global angle,mode
        global facecolors
        
        #start = time.ticks_ms()
        pen = (0,0,0)
        screen.fill(pen)
        
        i = 0
        oldt2 = 0
        # get each face (3d triangle)
        for face in faces:
            triangle = []
            for pointindex in face:
                point3 = points[pointindex]
                rotated3 = rot3d(point3,[angle,0,angle])
                triangle.append (rotated3)      
            
            # find normal of triangle 
            n = normal(triangle)
            camera = (0,0,10)
            d = dotproduct(n,camera)
            
            #hidden surface removal
            #only draw if facing camera
            if (d > 0) : continue
            
            # 3d points to 2d screen
            t1,t2,t3 = triangle
            t1 = to2d(t1)
            t2 = to2d(t2)
            t3 = to2d(t3)
            
            if mode == 0:
                #wireframe
                # quad (merge 2 consecutive triangles)
                if (i % 2) :
                    pen = (255,255,255)
                    pygame.draw.polygon (screen,pen,(t2,t2old,t1,t3),2)
                t2old = t2
            if mode == 1:
                # shade by normal to screen camera
                d = abs(d) / 500
                d = int(d)
                pen = (d,d,d)
                #fpoly(t1,t2,t3)
                pygame.draw.polygon (screen,pen,(t2,t1,t3))
            if mode == 2:
                # solid colors for faces
                r,g,b = facecolors[i]
                pen  = (r,g,b)
                #fpoly(t1,t2,t3)    
                pygame.draw.polygon (screen,pen,(t2,t1,t3))
            i += 1
                
        #timetaken = time.ticks_ms() - start
        #txt = " " + str (timetaken) + " ms - " + str (1000 // timetaken) + " fps"
        pen = (255,255,255)
        #text (txt,0,0)
init()

while True:
	update(0)
	draw(0)
	pygame.time.delay(20)
	pygame.display.flip()
