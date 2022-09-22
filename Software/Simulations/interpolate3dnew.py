from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
def seq_sampling(row, res=10, method='linear'):
    #3D sequential along x and y (isocircles):
    x, y, z = row

    #  distance to origin for each point (support vectors lengths)
    point_distance = np.linalg.norm(row[(0,2),], axis=0)

    # isocircle radii
    max_radius = math.sqrt(x[-1]+y[-1])
    radii = np.linspace(0, max_radius, res)

    # last (distance to origin) inner data points per circle (start point of segments)
    start_per_radius = [np.max(np.where(point_distance <= radius)) for radius in radii]

    # initialize coords
    new_x = np.zeros_like(radii)
    new_y = np.zeros_like(radii)
    new_z = np.zeros_like(radii)

    # assign first an last known coordinates
    new_x[0], new_y[0] = x[0], y[0] # 0, 0
    new_x[-1], new_y[-1] = x[-1], y[-1] # 1, 1

    for radius, startpoint in enumerate(start_per_radius[1:-1]):
        
        radius += 1

        # span line segment with point O outside and point I inside of iso-circle
        endpoint = startpoint+1

        O_x = x[endpoint]
        O_y = y[endpoint]

        I_x  = x[startpoint]
        I_y  = y[startpoint]

        # coefficients
        a = (O_x-I_x)**2 + (O_y-I_y)**2
        b = 2*((O_x-I_x)*(I_y) + (O_y-I_y)*(I_y))
        c = (I_x)**2 + (I_y)**2 - radii[radius]**2

        # !radicant cannot be zero given:
        # each segment is defined by max point lying inside or on iso-circle and the next point
        # as both axis are monotonically (strict monotonically y) increasing the next point lies outside of the ico-circle
        # thus (in 2D) a segment is intersecting a circle by definition.
        t = 2*c / (- b - math.sqrt(b**2 - 4*a*c))

        #check if intersection lies on line segment / within boundaries of t [0,1]
        if (t >= 0) and (t <= 1):
            new_x[radius], new_y[radius] = (O_x - I_x)*t + I_x, (O_y-I_y)*t + I_y

    # interpolate new_y based on projected new_y
    new_z = interpolate.interp1d(y, z, kind='linear')(new_y[1:-1])

    # assign first an last known coordinates
    new_z = np.insert(new_z,0,z[0])
    new_z = np.append(new_z,z[-1])

    return  np.array([new_x, new_y, new_z])
seq_sampling([2,4,5],[3,2,6],[4,2,3])
