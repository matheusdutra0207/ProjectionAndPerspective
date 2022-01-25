import numpy as np
from stl import mesh
from numpy.linalg import multi_dot
from math import pi

from transformations import translation_matrix, intrinsicParameter_matrix, projection_matrix, rotationY_matrix, rotationZ_matrix

class Coordinate:
    def __init__(self):
        self._e1 = np.array([[1],[0],[0],[0]]) # X
        self._e2 = np.array([[0],[1],[0],[0]]) # Y
        self._e3 = np.array([[0],[0],[1],[0]]) # Z
        self._base = np.hstack((self._e1, self._e2, self._e3))
        self._point = np.array([[0],[0],[0],[1]]) #origin point
        self.obj = np.eye(4)
        self.obj[:,:3] = self._base
        self.obj[:,-1] = self._point.T
        self._transformations = multi_dot([translation_matrix(dx=7, dy=0, dz=0), rotationY_matrix(-pi/2), rotationZ_matrix(pi/2)])
        self.obj = np.dot(self._transformations, self.obj)
        self._projection = projection_matrix()
        self._coordinateBox()

    def transformationCoordinate_ObjectReference(self, M):
        self._transformations_inv = np.linalg.inv(self._transformations)
        M1 = multi_dot([self._transformations,      
                        M, 
                        self._transformations_inv])
        self.obj = np.dot(M1, self.obj)
        self._transformations = multi_dot([self._transformations, M])
        self._coordinateBox()

    def transformationCoordinate_WorldReference(self, M): 
        self.obj = np.dot(M, self.obj)
        self._transformations = multi_dot([M, self._transformations])
        self._coordinateBox()

    def imageCoordinate(self, Object_Stl, intrinsicParameter):
        self._transformations_inv = np.linalg.inv(self._transformations)
        image = multi_dot([intrinsicParameter, 
                        self._projection,
                        self._transformations_inv, 
                        Object_Stl.mesh_homogeneous])
                        
        for i in range(0, len(image[2])):
            image[0][i] = image[0][i]/image[2][i]
            image[1][i] = image[1][i]/image[2][i]
            image[2][i] = image[2][i]/image[2][i]

        self.image = image   
        return self.image

    def _coordinateBox(self):
        self.obj_box = np.array([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1],[-1,-1,1],[1,1,1],[-1,1,1],[1,-1,1]])
        self.obj_box = np.vstack((self.obj_box.T,np.ones(self.obj_box.shape[0])))
        self.obj_box = np.dot(self._transformations, self.obj_box)

    def reset(self):
        self.__init__()
        

class Object_Stl:

    def __init__(self, name):
        # Load the STL files and add the vectors to the plot
        self._mesh = mesh.Mesh.from_file(f'stlFile/{name}.stl')
        # Get the x, y, z coordinates contained in the mesh structure that are the 
        # vertices of the triangular faces of the object
        self._x = self._mesh.x.flatten()
        self._y = self._mesh.y.flatten()
        self._z = self._mesh.z.flatten()
        # Get the vectors that define the triangular faces that form the 3D object
        self.mesh_vectors = self._mesh.vectors
        # Create the 3D object from the x,y,z coordinates and add the additional array of ones to 
        # represent the object using homogeneous coordinates
        self.mesh_homogeneous = np.array([
                                        self._x.T,
                                        self._y.T,
                                        self._z.T,
                                        np.ones(self._x.size)])