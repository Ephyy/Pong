# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-2
Drawing many cars in 2D using scene_graph2
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es


def createLine():

    gpuWhiteQuad = es.toGPUShape(bs.createColorQuad(1,1,1))
    
    # Cheating a single wheel
    line = sg.SceneGraphNode("line")
    line.childs += [gpuWhiteQuad]

    return line

def createLines(N):

    # First we scale a car
    scaledLine = sg.SceneGraphNode("traslatedLine")
    scaledLine.transform = tr.scale(0.01,0.15,0.0)
    scaledLine.childs += [createLine()] # Re-using the previous function

    lines = sg.SceneGraphNode("lines")

    baseName = "scaledLine"
    for i in range(N):
        # A new node is only locating a scaledCar in the scene depending on index i
        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr.translate(0.0, 0.9 - 0.3 * i, 0)
        newNode.childs += [scaledLine]

        # Now this car is added to the 'cars' scene graph
        lines.childs += [newNode]

    return lines

def createCero():

    gpuWhiteQuad = es.toGPUShape(bs.createColorQuad(1,1,1))

    line1 = sg.SceneGraphNode("line1")
    line1.transform = tr.matmul([
        tr.translate(0, 0.1, 0),
        tr.scale(0.1, 0.05, 1)
    ])
    line1.childs += [gpuWhiteQuad]

    line2 = sg.SceneGraphNode("line2")
    line2.transform = tr.matmul([
        tr.translate(0.05, 0, 0),
        tr.scale(0.05, 0.25, 1)
    ])
    line2.childs += [gpuWhiteQuad]
    
    line3 = sg.SceneGraphNode("line3")
    line3.transform = tr.matmul([
        tr.translate(0, -0.1, 0),
        tr.scale(0.1, 0.05, 1)
    ])
    line3.childs += [gpuWhiteQuad]

    line4 = sg.SceneGraphNode("line4")
    line4.transform = tr.matmul([
        tr.translate(-0.05, 0, 0),
        tr.scale(0.05, 0.25, 1)
    ])
    line4.childs += [gpuWhiteQuad]

    cero = sg.SceneGraphNode("cero")
    cero.childs += [line1]
    cero.childs += [line2]
    cero.childs += [line3]
    cero.childs += [line4]

    return cero

def createUno():

    gpuWhiteQuad = es.toGPUShape(bs.createColorQuad(1,1,1))

    line1 = sg.SceneGraphNode("line1")
    line1.transform = tr.scale(0.05, 0.25, 1)
    line1.childs += [gpuWhiteQuad]

    line2 = sg.SceneGraphNode("line2")
    line2.transform = tr.matmul([
        tr.translate(-0.05, 0.07, 0),
        tr.rotationZ(np.deg2rad(45)),
        tr.scale(0.1, 0.05, 1)
    ])
    line2.childs += [gpuWhiteQuad]

    uno = sg.SceneGraphNode("uno")
    uno.childs += [line1]
    uno.childs += [line2]

    return uno

def createDos():
    
    gpuWhiteQuad = es.toGPUShape(bs.createColorQuad(1,1,1))

    line1 = sg.SceneGraphNode("line1")
    line1.transform = tr.matmul([
        tr.translate(0, -0.1, 0),
        tr.scale(0.15, 0.05, 1)
    ])
    line1.childs += [gpuWhiteQuad]

    line2 = sg.SceneGraphNode("line2")
    line2.transform = tr.matmul([
        tr.translate(-0.05, -0.0625, 0),
        tr.scale(0.05, 0.125, 1)
    ])
    line2.childs += [gpuWhiteQuad]

    line3 = sg.SceneGraphNode("line3")
    line3.transform = tr.matmul([
        tr.scale(0.15, 0.05, 1)
    ])
    line3.childs += [gpuWhiteQuad]

    line4 = sg.SceneGraphNode("line4")
    line4.transform = tr.matmul([
        tr.translate(0.05, 0.0625, 0),
        tr.scale(0.05, 0.125, 1)
    ])
    line4.childs += [gpuWhiteQuad]

    line5 = sg.SceneGraphNode("line5")
    line5.transform = tr.matmul([
        tr.translate(0, 0.1, 0),
        tr.scale(0.15, 0.05, 1)
    ])
    line5.childs += [gpuWhiteQuad]

    dos = sg.SceneGraphNode("dos")
    dos.childs += [line1]
    dos.childs += [line2]
    dos.childs += [line3]
    dos.childs += [line4]
    dos.childs += [line5]

    return dos

def createTres():
    gpuWhiteQuad = es.toGPUShape(bs.createColorQuad(1,1,1))

    line1 = sg.SceneGraphNode("line1")
    line1.transform = tr.matmul([
        tr.translate(0, 0.1, 0),
        tr.scale(0.1, 0.05, 1)
    ])
    line1.childs += [gpuWhiteQuad]

    line2 = sg.SceneGraphNode("line2")
    line2.transform = tr.matmul([
        tr.translate(0.05, 0, 0),
        tr.scale(0.05, 0.25, 1)
    ])
    line2.childs += [gpuWhiteQuad]
    
    line3 = sg.SceneGraphNode("line3")
    line3.transform = tr.matmul([
        tr.translate(0, -0.1, 0),
        tr.scale(0.1, 0.05, 1)
    ])
    line3.childs += [gpuWhiteQuad]

    line4 = sg.SceneGraphNode("line4")
    line4.transform = tr.matmul([
        tr.scale(0.1, 0.05, 1)
    ])
    line4.childs += [gpuWhiteQuad]

    tres = sg.SceneGraphNode("tres")
    tres.childs += [line1]
    tres.childs += [line2]
    tres.childs += [line3]
    tres.childs += [line4]

    return tres


def createNumbers():

    numbers = sg.SceneGraphNode("Numbers")

    baseName = "traslatedNumber"
    for i in range(2):

        # First we scale a car
        scaledNumber = sg.SceneGraphNode("scaledNumber" + str(i))
        scaledNumber.transform = tr.uniformScale(0.6)
        scaledNumber.childs += [createCero()] # Re-using the previous function

        # A new node is only locating a scaledCar in the scene depending on index i
        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr.translate(0.4 * i - 0.2, 0.8 , 0)
        newNode.childs += [scaledNumber]

        # Now this car is added to the 'cars' scene graph
        numbers.childs += [newNode]

    return numbers
