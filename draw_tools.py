from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import multivariate_normal

def sph2cart(r, theta, phi):
    '''spherical to Cartesian transformation.'''
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z

def sphview(ax):
    '''returns the camera position for 3D axes in spherical coordinates'''
    r = np.square(np.max([ax.get_xlim(), ax.get_ylim()], 1)).sum()
    theta, phi = np.radians((90-ax.elev, ax.azim))
    return r, theta, phi

def ravzip(*itr):
    '''flatten and zip arrays'''
    return zip(*map(np.ravel, itr))




def draw(xpos, ypos, zpos, dx, dy, dz, e, threshold = 0):

    # print('Drawing', xpos, ypos, zpos, e)
    print('Length', len(xpos))


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=10., azim=130) #130 or 90

    # fig.set_figheight(15)
    # fig.set_figwidth(15)
    
    # Get the camera's location in Cartesian coordinates.
    x1, y1, z1 = sph2cart(*sphview(ax))
    camera = np.array((x1,y1,0))
    # Calculate the distance of each bar from the camera.
    #z_order = np.multiply([xpos,ypos, np.zeros_like(xpos)],camera).sum(0)
    z_order = xpos*camera[0]+ypos*camera[1]

    import matplotlib.colors as cl
    import matplotlib.cm as cm
    
    e = e + np.abs(e.min())
    fracs = e.astype(float)/e.max()
    norm = cl.Normalize(fracs.min(), fracs.max())
    color_values = cm.jet(norm(fracs.tolist()))

    for i, (x, y, z, dx, dy, dz, e) in enumerate(ravzip(xpos, ypos, zpos, dx, dy, dz, e)):
        if fracs[i] < threshold: continue
        pl = ax.bar3d(x, y, z, dx, dy, dz, color=color_values[i], alpha = 0.5)# 'salmon', alpha=alp, zsort='max') #, edgecolor='black')
        pl._sort_zpos = z_order[i]
        


    # plt.tick_params(labelsize=15)
    # plt.tick_params(axis='z', pad=7)
    ax.set_xlabel(r'x', fontsize=15, labelpad=25)
    ax.set_ylabel(r'y', fontsize=15, labelpad=25)
    ax.set_zlabel(r'z', fontsize=15, labelpad=25)    

    # ax.set_xlim3d(-225, 225)
    # ax.set_ylim3d(-225, 225)
    # ax.set_zlim3d(0, 550)

    # proxy0 = plt.Rectangle((0, 0), 1, 1, fc="w")
    # proxy1 = plt.axvline(x = 1, color='firebrick')
    # proxy2 = plt.Rectangle((0, 0), 1, 1, fc="salmon")
    # ax.legend([proxy0, proxy1,proxy2],['MicroBooNE 1.6e20 POT', 'Measured','Stat + Syst Uncertainties'], fontsize=20,loc=1)






