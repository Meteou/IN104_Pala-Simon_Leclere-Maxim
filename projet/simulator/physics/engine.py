from ..utils.vector import Vector, Vector2
from .constants import G, m




def gravitational_force(pos1, mass1, pos2, mass2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
    normF=(G*(mass1*mass2))/Vector.norm(Vector.__sub__(pos1, pos2))**2
    VectDirecteur=[(pos2[0]-pos1[0])/Vector.norm(Vector.__sub__(pos1, pos2)),(pos2[1]-pos1[1])/Vector.norm(Vector.__sub__(pos1, pos2))]
    Force2sur1=[normF*VectDirecteur[0],normF*VectDirecteur[1]]
    
    return Force2sur1
        
    


class IEngine:
    def __init__(self, world):
        self.world = world

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
        n=len(y0)
        yp=[0]*n
        for i in range(n/2):
            yp[i]=y0[n/2+i]
        for i in range(n/4):
            ax=[0,0]
            for j in range((n/4)-1):
                if (j!=i):
                    ax = ax +[(1/m)* gravitational_force([y0[i],y0[i+1]], m,[y0[j],y0[j+1]], m)]
            yp[n/2+i]=ax[0]
            yp[n/2+i+1]=ax[1]
        return yp
        
                
    
            
        

    def make_solver_state(self):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the 
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """
        y0=[]
        for body in self.world.bodies:
            y0.append(body.position[0])
            y0.append(body.position[1])
            
        for body in self.world.bodies:
            y0.append(body.velocity[0])
            y0.append(body.velocity[1])


class DummyEngine(IEngine):
    pass
