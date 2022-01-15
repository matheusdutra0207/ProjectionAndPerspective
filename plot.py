import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d
from numpy import mean

class Plot:

    def __init__(self, limit=[-6, 6], figsize=(10,10)):
        self.figure = plt.figure(figsize=figsize)
        self.ax = self.figure.add_subplot(projection='3d')
        self.ax.set_title("World")
        self.ax.set_xlim(limit)
        self.ax.set_xlabel("x axis")
        self.ax.set_ylim(limit)
        self.ax.set_ylabel("y axis")
        self.ax.set_zlim(limit)
        self.ax.set_zlabel("z axis")

    #adding quivers to the plot
    def draw_arrows(self, point, base, length=1.5):
        # The object base is a matrix, where each column represents the vector 
        # of one of the axis, written in homogeneous coordinates (ax,ay,az,0)    
        # Plot vector of x-axis
        self.ax.quiver(point[0],point[1],point[2],base[0,0],base[1,0],base[2,0],color='red',pivot='tail',  length=length)
        # Plot vector of y-axis
        self.ax.quiver(point[0],point[1],point[2],base[0,1],base[1,1],base[2,1],color='green',pivot='tail',  length=length)
        # Plot vector of z-axis
        self.ax.quiver(point[0],point[1],point[2],base[0,2],base[1,2],base[2,2],color='blue',pivot='tail',  length=length)

    def _set_axes_equal(self):
        #Make axes of 3D plot have equal scale so that spheres appear as spheres,
        #cubes as cubes, etc..  This is one possible solution to Matplotlib's
        #ax.set_aspect('equal') and ax.axis('equal') not working for 3D.
        #Input
        #  ax: a matplotlib axis, e.g., as output from plt.gca().  
        x_limits = self.ax.get_xlim3d()
        y_limits = self.ax.get_ylim3d()
        z_limits = self.ax.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        x_middle = mean(x_limits)
        y_range = abs(y_limits[1] - y_limits[0])
        y_middle = mean(y_limits)
        z_range = abs(z_limits[1] - z_limits[0])
        z_middle = mean(z_limits)

        # The plot bounding box is a sphere in the sense of the infinity
        # norm, hence I call half the max range the plot radius.
        plot_radius = 0.5*max([x_range, y_range, z_range])

        self.ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
        self.ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
        self.ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])


    def draw_stl(self, Object_stl, elev=25, azim=-35, dist=10):
        # Plot and render the faces of the object
        self.ax.add_collection3d(art3d.Poly3DCollection(Object_stl.mesh_vectors))
        # Plot the contours of the faces of the object
        self.ax.add_collection3d(art3d.Line3DCollection(Object_stl.mesh_vectors, colors='k', linewidths=0.2, linestyles='-'))
        # Plot the vertices of the object
        # Set axes and their aspect
        self.ax.auto_scale_xyz( Object_stl.mesh_homogeneous[0,:],
                                Object_stl.mesh_homogeneous[1,:],
                                Object_stl.mesh_homogeneous[2,:])
        self._set_axes_equal()
        self.ax.view_init(elev=elev,azim=azim)
        self.ax.dist=dist


    def save_png(self, name='saved_figure'):
        self.figure.savefig(f'image/{name}.png')