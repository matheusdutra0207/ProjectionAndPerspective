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