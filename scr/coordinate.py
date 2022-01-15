import numpy as np
from stl import mesh

from transformations import translation_matrix

class Coordinate:
    def __init__(self):
        self._e1 = np.array([[1],[0],[0],[0]]) # X
        self._e2 = np.array([[0],[1],[0],[0]]) # Y
        self._e3 = np.array([[0],[0],[1],[0]]) # Z
        self.base = np.hstack((self._e1, self._e2, self._e3))
        self.point = np.array([[0],[0],[0],[1]]) #origin point
        self._transformations = translation_matrix(dx=0, dy=0, dz=0)

    def moveCoordinate_ObjectReference(self, M): 
        self._transformations_inv = np.linalg.inv(self._transformations)
        self.point = np.dot(self._transformations_inv, self.point)
        self._transformations = np.dot(self._transformations, M)
        self.point = np.dot(self._transformations, self.point)

    def moveCoordinate_WorldReference(self, M): 
        self.point = np.dot(M, self.point)
        self._transformations = np.dot(self._transformations, M)
        
    def rotateCoordinate_ObjectReference(self, M): 
        self._transformations_inv = np.linalg.inv(self._transformations)
        self.base = np.dot(self._transformations_inv, self.base)
        self._transformations = np.dot(self._transformations, M)
        self.base = np.dot(self._transformations, self.base)

    def rotateCoordinate_WorldReference(self, M):
        self.point = np.dot(M, self.base)
        self._transformations = np.dot(self._transformations, M)

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