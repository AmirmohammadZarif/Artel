import math
import robot
class kinematics:
    def __init__(self):  
        '''
        #########
        Constants
        #########
        '''

        self.s      = 165*2
        self.sqrt3  = math.sqrt(3.0)
        self.pi     = 3.141592653
        self.sin120 = self.sqrt3 / 2.0
        self.cos120 = -0.5
        self.tan60  = self.sqrt3
        self.sin30  = 0.5
        self.tan30  = 1.0 / self.sqrt3

        '''
        #################################
        Delta Robot Kinematics parameters
        Initializing Physical Parameters
        - rf : Distance from motor shaft to elbow
        - f  : Base radius - Distance from center of machine base to center of each motor shaft. 
                More than likely this is the middle of the side of a triangle, NOT the corner.
        - re : Distrance from elbow to the wrist
        - e : Distance from wrists to the center of the hand
        - b : Base to floor distance
        #################################
        '''
        
        self.e  =  45.0
        self.f  =  150.0
        # self.re =  277.0 
        self.re =  470.0
        self.rf =  150.0
        self.bp = 900
        self.cp = 0


    '''
    ##################
    Forward kinematics (theta1, theta2, theta3)
    ##################
    '''
    def forward(self,theta1, theta2, theta3):
        x0 = 0.0
        y0 = 0.0
        z0 = 0.0
        
        t = (self.f-self.e) * self.tan30 / 2.0
        dtr = self.pi / 180.0
        
        theta1 *= dtr
        theta2 *= dtr
        theta3 *= dtr
        
        y1 = -(t + self.rf*math.cos(theta1) )
        z1 = -self.rf * math.sin(theta1)
        
        y2 = (t + self.rf*math.cos(theta2)) * self.sin30
        x2 = y2 * self.tan60
        z2 = -self.rf * math.sin(theta2)
        
        y3 = (t + self.rf*math.cos(theta3)) * self.sin30
        x3 = -y3 * self.tan60
        z3 = -self.rf * math.sin(theta3)
        
        dnm = (y2-y1)*x3 - (y3-y1)*x2
        
        w1 = y1*y1 + z1*z1
        w2 = x2*x2 + y2*y2 + z2*z2
        w3 = x3*x3 + y3*y3 + z3*z3
        
        # x = (a1*z + b1)/dnm
        a1 = (z2-z1)*(y3-y1) - (z3-z1)*(y2-y1)
        b1= -( (w2-w1)*(y3-y1) - (w3-w1)*(y2-y1) ) / 2.0
        
        # y = (a2*z + b2)/dnm
        a2 = -(z2-z1)*x3 + (z3-z1)*x2
        b2 = ( (w2-w1)*x3 - (w3-w1)*x2) / 2.0
        
        # a*z^2 + b*z + c = 0
        a = a1*a1 + a2*a2 + dnm*dnm
        b = 2.0 * (a1*b1 + a2*(b2 - y1*dnm) - z1*dnm*dnm)
        c = (b2 - y1*dnm)*(b2 - y1*dnm) + b1*b1 + dnm*dnm*(z1*z1 - self.re*self.re)
        
        # discriminant
        d = b*b - 4.0*a*c
        if d < 0.0:
            return [1,0,0,0] # non-existing povar. return error,x,y,z
        
        z0 = -0.5*(b + math.sqrt(d)) / a
        x0 = (a1*z0 + b1) / dnm
        y0 = (a2*z0 + b2) / dnm

        return [0,x0,y0,z0]

    '''
    ##################
    Inverse kinematics (x, y, z)
    ##################
    '''
    def angle_yz(self, x0, y0, z0, theta=None):
        y1 = -0.5*0.57735*self.f # f/2 * tg 30
        y0 -= 0.5*0.57735*self.e # shift center to edge
        # z = a + b*y
        a = (x0*x0 + y0*y0 + z0*z0 + self.rf * self.rf - self.re*self.re - y1*y1) / (2.0*z0)
        b = (y1-y0) / z0

        # discriminant
        d = -(a + b*y1)*(a + b*y1) + self.rf * (b*b*self.rf + self.rf)
        if d<0:
            return [1,0] # non-existing povar.  return error, theta

        yj = (y1 - a*b - math.sqrt(d)) / (b*b + 1) # choosing outer povar
        zj = a + b*yj
        theta = math.atan(-zj / (y1-yj)) * 180.0 / self.pi + (180.0 if yj>y1 else 0.0)
        
        return [0,theta] # return error, theta

    def inverse(self, x0, y0, z0):
        theta1 = 0
        theta2 = 0
        theta3 = 0
        status = self.angle_yz(x0,y0,z0)

        if status[0] == 0:
            theta1 = status[1]
            status = self.angle_yz(x0*self.cos120 + y0*self.sin120,
                                    y0*self.cos120-x0*self.sin120,
                                    z0,
                                    theta2)
        if status[0] == 0:
            theta2 = status[1]
            status = self.angle_yz(x0*self.cos120 - y0*self.sin120,
                                    y0*self.cos120 + x0*self.sin120,
                                    z0,
                                    theta3)
        theta3 = status[1]

        return [status[0],theta1,theta2,theta3]