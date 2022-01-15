from math import pi

from coordinate import Coordinate, Object_Stl
from plot import Plot
from transformations import translation_matrix, rotationZ_matrix, rotationX_matrix, rotationY_matrix

if __name__ == '__main__':
    R = rotationY_matrix(-pi/2)
    T = translation_matrix(dx=5)

    origin = Coordinate()
    camera = Coordinate()
    camera.moveCoordinate_ObjectReference(T)
    camera.rotateCoordinate_ObjectReference(R)

    plot = Plot()
    plot.draw_arrows(origin.point, origin.base)
    T = translation_matrix(dx=5)
    camera.moveCoordinate_ObjectReference(T)
    T = translation_matrix(dx=5)
    camera.moveCoordinate_WorldReference(T)
    plot.draw_arrows(camera.point, camera.base)
    house = Object_Stl(name = "WoodHouse")
    plot.draw_stl(house)
    plot.save_png(name = "world")