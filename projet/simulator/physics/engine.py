from ..utils.vector import Vector, Vector2
from .constants import G

from math import acos, asin, atan, cos, sin, tan, pi, sqrt, floor
from numpy import array, dot, transpose
from simulator.graphics import Screen

screen_size = Vector2(800, 600)
screen = Screen(screen_size,
                    bg_color=(0, 0, 0),
                    caption="Simulator")

def gravitational_force(pos1, mass1, pos2, mass2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
    r=Vector.norm(pos1-pos2)
    Force2sur1=(-G*mass1*mass2/(r*r*r))*(pos1-pos2)
    return Force2sur1

def Rotation(theta, v):
    R=array([[cos(theta), -sin(theta)], [sin(theta),cos(theta)]])
    return dot(R,transpose(v))


class IEngine:
    def __init__(self, world):
        self.world = world
        self.n=len(self.world)
        if self.n>0 :
            self.dim=len(self.world._bodies[0].position)

    def derivatives(self, t0, y0):
        """ This is the method that will be fed to the solver
            it does not use it's first argument t0,
            its second argument y0 is a vector containing the positions
            and velocities of the bodies, it is laid out as follow
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.

            Return the derivative of the state, it is laid out as follow
                [vx1, vy1, vx2, vy2, ..., vxn, vyn, ax1, ay1, ax2, ay2, ..., axn, ayn]
            where vxi, vyi are the velocities and axi, ayi are the accelerations.
        """

        raise NotImplementedError



    def make_solver_state(self):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """
        raise NotImplementedError



class DummyEngine(IEngine):

    def derivatives(self, t0, y0):
        yp=Vector(self.n*2*self.dim)
        
        for i in range(self.n):
            #On reprend les vecteurs Vitesses de base qui se trouvent dans y0
            
            yp[self.dim*i]= y0[(self.n + i)*self.dim]
            yp[self.dim*i+1]= y0[(self.n + i)*self.dim+1]
            
            ax=Vector2(0,0)
            for j in range(self.n):
                if(i!=j):
                    ax += gravitational_force(Vector2(y0[self.dim*i],y0[self.dim*i+1]), 1, Vector2(y0[self.dim*j],y0[self.dim*j+1]), self.world._bodies[j].mass)
            
            yp[self.dim*self.n + self.dim*i ] = ax.get_x()
            yp[self.dim*self.n + self.dim*i+1]= ax.get_y()
            
        return yp


    def make_solver_state(self):
        y=Vector(4*self.n)

        for i in range(self.n):
            y[self.dim*i]= self.world._bodies[i].position.get_x()
            y[self.dim*i+1]= self.world._bodies[i].position.get_y()
            y[self.dim*self.n + self.dim*i ] = self.world._bodies[i].velocity.get_x()
            y[self.dim*self.n + self.dim*i+1]= self.world._bodies[i].velocity.get_y()
        return y


class AvecCollison(DummyEngine):
    
    def derivatives(self, t0, y0):
        self.n=len(self.world)

        yp=Vector(len(y0)) 
        vect_acc=Vector2(0,0)

        for i in range(self.n):

            print(i)
            corpsi=self.world._bodies[i]
            
            yp[self.dim*i]= y0[(self.n + i)*self.dim]
            yp[self.dim*i+1]= y0[(self.n + i)*self.dim+1]
            pos_i=Vector2(y0[self.dim*i],y0[self.dim*i+1])

            
        
            for j in range(i):
                
    
                vect_diff=pos_i - Vector2(y0[self.dim*j],y0[self.dim*j+1])
                d=vect_diff.norm()
                    
                corpsj=self.world._bodies[j]
                
                
                rij=(self.world._bodies[j].position-self.world._bodies[i].position)
                uij=Vector.norm(rij)*50
                
                
                ri=corpsi.draw_radius
                rj=corpsj.draw_radius
                
                R=ri+rj
                
    
                print(uij<R)
                print(uij)
                if uij<R:
                        
                    eij=rij/uij
                    nij=Rotation(pi/2,eij) #calcul 
                    
                    mi=corpsi.mass
                    mj=corpsj.mass
                    
                    c11=(mi-mj)/(mi+mj)
                    c12=(2*mj/(mi+mj))
                    c21=(mj-mi)/(mi+mj)
                    c22=(2*mi)/(mi+mj)
                    
                    
             
                    vi=Vector2(y0[(self.n + i)*self.dim],y0[(self.n + i)*self.dim+1])
                    
                    vj=Vector2(y0[(self.n + j)*self.dim],y0[(self.n + j)*self.dim+1])

                    thetai=acos(dot(vi,nij)/Vector.norm(vi)) #angles de collision
                    thetaj=acos(dot(vj,nij)/Vector.norm(vj))
                    
                    
                    
                    thetapi=atan(c11*tan(thetai)+c12*Vector.norm(vj)*sin(thetaj)/(cos(thetai)*Vector.norm(vi))) #angles de rebond
                    thetapj=atan(c21*tan(thetaj)+c22*Vector.norm(vi)*sin(thetai)/(cos(thetaj)*Vector.norm(vj)))
                    
                    
                    
                    vpi=sqrt((Vector.norm(vj)*c12*sin(thetaj)+c11*Vector.norm(vi)*sin(thetai))**2+Vector.norm(vi)*Vector.norm(vi)*cos(thetai)*cos(thetai)) #vitesse de rebond
                    vpj=sqrt((Vector.norm(vi)*c22*sin(thetai)+c21*Vector.norm(vj)*sin(thetaj))**2+Vector.norm(vj)*Vector.norm(vj)*cos(thetaj)*cos(thetaj))
                   
                    
                    
                    print(vpi)
                    print(vpj)
                    
                    y0[(self.n + i-1)*self.dim] = -vpi
                    y0[(self.n + i)*self.dim-1] = vpi
                    y0[self.dim*self.n + self.dim*(j+1) ] = vpj
                    y0[self.dim*self.n + self.dim*(j+1)+1 ] = -vpj
                    
                    
                    
                    
                    

    

                else:
                            vect_acc=(-G/(d*d*d))*vect_diff
                            yp[self.dim*self.n + self.dim*i ] += self.world._bodies[j].mass*vect_acc.get_x()
                            yp[self.dim*self.n + self.dim*i+1]+= self.world._bodies[j].mass*vect_acc.get_y()
                            yp[self.dim*self.n + self.dim*j ] += -self.world._bodies[i].mass*vect_acc.get_x()
                            yp[self.dim*self.n + self.dim*j+1]+= -self.world._bodies[i].mass*vect_acc.get_y()
                            print(yp)

        return yp
                            



