import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  
import numpy as np
from math import pi,cos,sin

def translation_matrix(dx=0, dy=0, dz=0):
  T = np.array([[1, 0, 0, dx],
               [0, 1, 0,  dy],
               [0, 0, 1,  dz],
               [0, 0, 0,  1]])
  return T

def rotationZ_matrix(angle_rad):
  R_homogeneous = np.array([ 
               [cos(angle_rad), -sin(angle_rad), 0, 0],
               [sin(angle_rad),  cos(angle_rad), 0, 0],
               [0             ,  0             , 1, 0],
               [0             ,  0             , 0, 1]
            ])
  return R_homogeneous

def rotationX_matrix(angle_rad):
  R_homogeneous = np.array([ 
               [1 ,  0             ,  0,              0],
               [0 ,  cos(angle_rad), -sin(angle_rad), 0],
               [0 ,  sin(angle_rad),  cos(angle_rad), 0],
               [0 ,  0             ,  0             , 1]
            ])
  return R_homogeneous

def rotationY_matrix(angle_rad):
  R_homogeneous = np.array([ 
               [cos(angle_rad) ,  0  ,  sin(angle_rad),   0],
               [0              ,  1  ,  0             ,   0],
               [-sin(angle_rad),  0  ,  cos(angle_rad),   0],
               [0              ,  0  ,  0             ,   1]
            ])
  return R_homogeneous 

class Coordinate:
    def __init__(self):
        self._e1 = np.array([[1],[0],[0],[0]]) # X
        self._e2 = np.array([[0],[1],[0],[0]]) # Y
        self._e3 = np.array([[0],[0],[1],[0]]) # Z
        self.base = np.hstack((self._e1, self._e2, self._e3))
        self.point = np.array([[0],[0],[0],[1]]) #origin point
        self.transformations = translation_matrix(dx=0, dy=0, dz=0)

    def moveCoordinate(self, M):
        self.transformations_inv = np.linalg.inv(self.transformations)
        self.point = np.dot(self.transformations_inv, self.point)
        self.transformations = np.dot(self.transformations, M)
        self.point = np.dot(self.transformations, self.point)
        
    def rotateCoordinate(self, M):
        self.transformations_inv = np.linalg.inv(self.transformations)
        self.base = np.dot(self.transformations_inv, self.base)
        self.transformations = np.dot(self.transformations, M)
        self.base = np.dot(self.transformations, self.base)

class House:
    pass

if __name__ == '__main__':
    origin = Coordinate()
    camera = Coordinate()