from math import pi
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
import datetime

from coordinate import Coordinate, Object_Stl
from plot import Plot, PlotImage
from transformations import translation_matrix, rotationZ_matrix, rotationX_matrix, rotationY_matrix, intrinsicParameter_matrix

def update_label():
    pixmap_world = QPixmap('image/world.png')
    pixmap_projection = QPixmap('image/projection.png')
    interface.world.setPixmap(pixmap_world)
    interface.projection.setPixmap(pixmap_projection)
    interface.camera_world.setText(f"x_cam = {int(camera.obj[:,-1].T[0])} y_cam = {int(camera.obj[:,-1].T[1])} z_cam = {int(camera.obj[:,-1].T[2])}")

def resetInterface():
    # getting the interface values 
    f = int(interface.spinBox_f.text())
    sx = int(interface.spinBox_sx.text())
    sy = int(interface.spinBox_sy.text())
    s0 = int(interface.spinBox_s0.text())
    ox = int(interface.spinBox_ox.text())
    oy = int(interface.spinBox_oy.text())
    limitWorld = int(interface.spinBox_limitWorld.text())
    limitProjection = int(interface.spinBox_limitProjection.text())
    elev = int(interface.spinBox_elv.text())
    azim = int(interface.spinBox_azim.text())
    dist = int(interface.spinBox_dist.text())

    camera.reset()

    plot = Plot(limit=[-limitWorld, limitWorld])
    plot.draw_arrows(camera.obj[:,3], camera.obj[:,0:3])
    plot.draw_obj(camera.obj_box)
    plot.draw_stl(Object_stl = house,elev = elev, azim = azim, dist = dist)
    plot.save_png(name = "world")
    intrinsicParameter = intrinsicParameter_matrix( f=f, 
                                                    sX = sx,
                                                    sY = sy,
                                                    sTheta = s0,
                                                    oX = ox,
                                                    oY = oy
                                                    )

    house_image = camera.imageCoordinate(Object_Stl = house, intrinsicParameter = intrinsicParameter)
    plot_image = PlotImage( image = house_image, 
                            limit=[-limitProjection, limitProjection],
                            image_name = 'projection')

def activateInterface():
    # getting the interface values    
    angle_grades = int(interface.spinBox_rotation.text())
    move = int(interface.spinBox_traslation.text())
    f = int(interface.spinBox_f.text())
    sx = int(interface.spinBox_sx.text())
    sy = int(interface.spinBox_sy.text())
    s0 = int(interface.spinBox_s0.text())
    ox = int(interface.spinBox_ox.text())
    oy = int(interface.spinBox_oy.text())
    limitWorld = int(interface.spinBox_limitWorld.text())
    limitProjection = int(interface.spinBox_limitProjection.text())
    elev = int(interface.spinBox_elv.text())
    azim = int(interface.spinBox_azim.text())
    dist = int(interface.spinBox_dist.text())

    if interface.radioButton_camera.isChecked():
        if interface.radioButton_rotX.isChecked():
            angle_rad = (angle_grades*pi)/180
            R = rotationX_matrix(angle_rad)
            camera.transformationCoordinate_ObjectReference(R)

        elif interface.radioButton_rotY.isChecked():
            angle_rad = (angle_grades*pi)/180
            R = rotationY_matrix(angle_rad)
            camera.transformationCoordinate_ObjectReference(R)

        elif interface.radioButton_rotZ.isChecked():
            angle_rad = (angle_grades*pi)/180
            R = rotationZ_matrix(angle_rad)
            camera.transformationCoordinate_ObjectReference(R)

        elif interface.radioButton_transX.isChecked():
            T = translation_matrix(dx=move)
            camera.transformationCoordinate_ObjectReference(T)

        elif interface.radioButton_transY.isChecked():
            T = translation_matrix(dy=move)
            camera.transformationCoordinate_ObjectReference(T)

        elif interface.radioButton_transZ.isChecked():
            T = translation_matrix(dz=move)
            camera.transformationCoordinate_ObjectReference(T)

    elif interface.radioButton_world.isChecked():
        if interface.radioButton_rotX.isChecked():
            angle_rad = (angle_grades*pi)/180
            R = rotationX_matrix(angle_rad)
            camera.transformationCoordinate_WorldReference(R)

        elif interface.radioButton_rotY.isChecked():
            angle_rad = (angle_grades*pi)/180
            R = rotationY_matrix(angle_rad)
            camera.transformationCoordinate_WorldReference(R)

        elif interface.radioButton_rotZ.isChecked():
            angle_rad = (angle_grades*pi)/180
            R = rotationZ_matrix(angle_rad)
            camera.transformationCoordinate_WorldReference(R)

        elif interface.radioButton_transX.isChecked():
            T = translation_matrix(dx=move)
            camera.transformationCoordinate_WorldReference(T)

        elif interface.radioButton_transY.isChecked():
            T = translation_matrix(dy=move)
            camera.transformationCoordinate_WorldReference(T)

        elif interface.radioButton_transZ.isChecked():
            T = translation_matrix(dz=move)
            camera.transformationCoordinate_WorldReference(T)
    
    plot = Plot(limit=[-limitWorld, limitWorld])
    plot.draw_arrows(camera.obj[:,3], camera.obj[:,0:3])
    plot.draw_obj(camera.obj_box)
    plot.draw_stl(Object_stl = house,elev = elev, azim = azim, dist = dist)
    plot.save_png(name = "world")
    intrinsicParameter = intrinsicParameter_matrix( f=f, 
                                                    sX = sx,
                                                    sY = sy,
                                                    sTheta = s0,
                                                    oX = ox,
                                                    oY = oy
                                                    )

    house_image = camera.imageCoordinate(Object_Stl = house, intrinsicParameter = intrinsicParameter)
    plot_image = PlotImage( image = house_image, 
                            limit=[-limitProjection, limitProjection],
                            image_name = 'projection')

if __name__ == '__main__':
    # Define camera
    camera = Coordinate()

    # Define Object
    house = Object_Stl(name = "WoodHouse")

    # Define Projection in the image 
    intrinsicParameter = intrinsicParameter_matrix( f= 5, 
                                                    sX = 10,
                                                    sY = 10,
                                                    sTheta = 0,
                                                    oX = 0,
                                                    oY = 0
                                                )
    house_image = camera.imageCoordinate(Object_Stl = house, intrinsicParameter = intrinsicParameter)

    # Inicial Plot
    plot = Plot()
    plot.draw_arrows(camera.obj[:,3], camera.obj[:,0:3])
    plot.draw_obj(camera.obj_box)
    plot.draw_stl(Object_stl = house, elev=25, azim=-35, dist=9)
    plot.save_png(name = "world")
    plot_image = PlotImage( image = house_image, 
                            limit=[-30, 30],
                            image_name = 'projection')

    # Interface 
    app = QtWidgets.QApplication([])
    interface = uic.loadUi("interface.ui")
    interface.apply.clicked.connect(activateInterface)
    interface.reset.clicked.connect(resetInterface)
    interface.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(update_label)
    timer.start(10)  # every 10 milliseconds
    app.exec()