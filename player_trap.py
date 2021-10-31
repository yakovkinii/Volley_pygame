import pygame
import math
import numpy as np

class trap:
    def __init__(self,x0,y0,x1,y1,x2,y2,x3,y3, xc,yc,rot,color):
        #static
        self.pts0=np.array([[x0,y0],[x1,y1],[x2,y2],[x3,y3]]).astype(float) #points relative to the center
        self.color=color #color for display
        #static hardcoded
        self.m=1.0 #mass
        self.i=100.0 #inertia moment
        self.frict=0.2 #lateral friction
        self.frictw=10.0 #rotational friction
        #init static
        self.col_ball=[] #collision lines (given by indexes of 2 pts)
        self.col_floor=[] #collision points (by index)
        #dynamic
        self.center=np.array([xc,yc]) #center of mass
        self.rot=rot #rotation
        #init dynamic
        self.force_cm=np.array([0.0,0.0]) #force that acts on the center of mass
        self.force_mom=0.0 #force momentum
        self.v=np.array([0.0,0.0]) #lateral speed
        self.w=0.0 #angular speed
        #temp
        self.pts =np.array([[x0,y0],[x1,y1],[x2,y2],[x3,y3]]).astype(float) #points (absolute, temporary variable)
        #control
        self.ptschanged=True
    #one-time calls
    def add_ball_collision(self,v0,v1):
        self.col_ball.append([v0,v1])
    def add_floor_collision(self,v0):
        self.col_floor.append(v0)
    #helpers
    def get_center(self): 
        return self.center
    def rotatepts(self,angrad): #should be applied before move
        si=math.sin(angrad)
        co=math.cos(angrad)
        for i,r in enumerate(self.pts):
            xn=r[0]*co-r[1]*si
            yn=r[0]*si+r[1]*co
            self.pts[i][0]=xn
            self.pts[i][1]=yn
    def movepts(self,dr):
        for i,pt in enumerate(self.pts):
            self.pts[i]=pt+dr
    def update_pts(self):
        if(not self.ptschanged): 
            return
        self.pts=np.copy(self.pts0)
        self.rotatepts(self.rot)
        self.movepts(self.get_center())
        self.ptschanged=False
    def update_pts_force(self):
        self.ptschanged=True
        self.update_pts()
    def move(self,dr):
        self.center+self.center+dr
        self.ptschanged=True
    def rotate(self,angrad):
        self.rot=self.rot+angrad
        self.ptschanged=True
    #forces
    def add_momentum_force(self,force,n_pt):
        rc=self.get_center()
        rpt=self.pts[n_pt]
        rr=rpt-rc
        dm=force[1]*rr[0]-force[0]*rr[1]
        self.force_mom=self.force_mom+dm
    def add_momentum(self,dm):
        self.force_mom=self.force_mom+dm
    def add_force(self,force):
        self.force_cm=self.force_cm+force
    #draw
    def draw(self,screen):
        self.update_pts()
        # print(self.pts)
        pygame.draw.polygon(screen,self.color, self.pts)
    def draw_col(self,screen):
        self.update_pts()
        for l in self.col_ball:
            pygame.draw.line(screen, (255, 0, 0),self.pts[l[0]],self.pts[l[1]])
        for v in self.col_floor:
            pygame.draw.circle(screen, (255, 0, 0),self.pts[v],3)
