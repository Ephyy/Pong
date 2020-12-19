"""
Daniel Calderon, CC3501, 2019-1
Transformation matrices for computer graphics
v2.0
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import numeros as nr

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
INT_BYTES = 4

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.juego = False

controller = Controller()
space = 0

def on_key(window, key, scancode, action, mods):   
    global controller

    # Keep pressed buttons
    if (action != glfw.RELEASE):
        # Condicion de subir o bajar
        if key == glfw.KEY_UP:
            # Esta condicion es para que el jugador no siga subiendo y choque arriba y abajo
            # con la ventana
            if j1.y + j1.sizeY/2 <= 0.9:
                j1.y_ant = j1.y
                j1.y += 0.05
                j1.direccion = True
        if key == glfw.KEY_DOWN:
            if j1.y - j1.sizeY/2 >= -0.9:
                j1.y_ant = j1.y
                j1.y -= 0.05
                j1.direccion = False
        if key == glfw.KEY_W:
            if j2.y + j2.sizeY/2 <= 0.9:
                j2.y_ant = j2.y
                j2.y += 0.05
                j2.direccion = True
        if key == glfw.KEY_S:
            if j2.y - j2.sizeY/2 >= -0.9:
                j2.y_ant = j2.y
                j2.y -= 0.05
                j2.direccion = False    

    if action != glfw.PRESS:
        return

    # UWU
    elif key == glfw.KEY_SPACE:
        reiniciarJuego()

    elif key == glfw.KEY_1:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        sys.exit()
        
    else:
        print('Unknown key')


class GPUShape:
    def __init__(self):
        self.vao = 0
        self.vbo = 0
        self.ebo = 0
        self.texture = 0
        self.size = 0


def drawShape(shaderProgram, shape, transform):

    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # updating the new transform attribute
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_TRUE, transform)

    # Describing how the data is stored in the VBO
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    
    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # This line tells the active shader program to render the active element buffer with the given size
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)

# Funcion que crea una linea mediante grafo
def createLine():

    gpuWhiteQuad = es.toGPUShape(bs.createColorQuad(1,1,1))
    
    # Cheating a single line
    line = sg.SceneGraphNode("line")
    line.transform = tr.identity()
    line.childs += [gpuWhiteQuad]

    return line

# Funcion que crea n lineas mediante el uso de grafos
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

# Funcion para crear rectangulos
def createQuad(color, x, y):
    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape

    vertexData = np.array([
        #   positions        colors
        -0.5 + x, -0.5 + y, 0.0, color[0], color[1], color[2],
        0.5 + x, -0.5 + y, 0.0, 0, 0, 0,
        0.5 + x, 0.5 + y, 0.0, 0, 0, 0,
        -0.5 + x, 0.5 + y, 0.0, color[0], color[1], color[2]
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
        2, 3, 0], dtype=np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

# Clase de los jugadores
class Player:
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.sizeX = 0.05
        self.sizeY = 0.5
        self.shape = createQuad([1, 1, 1], 0, 0)
        self.aColisionado = False
        self.direccion = True

    def reset(self):
        self.y = 0.0
        self.aColisionado = False

# Clase de la bola
class Ball:
    def __init__(self):
        self.vx0 = -0.7
        self.vy0 = -0.2
        self.x = 0.0
        self.y = 0.0
        self.vX = self.vx0
        self.vY = self.vy0
        self.x_collision = 0.0
        self.y_collision = 0.0
        self.size = 0.06
        self.sizeX = self.size/1.6
        self.shape = createQuad([1, 1, 1], 0.0, 0.0)

    def reset(self):
        self.x = 0.0
        self.y = 0.0
        self.x_collision = 0.0
        self.y_collision = 0.0
        self.vX = self.vx0
        self.vY = self.vy0
        glfw.set_time(0)

# Clase para dibujar rectangulo xD (para el mapa)
class Rectangulo:
    def __init__(self, x, y, sizeX, sizeY):
        self.x = x
        self.y = y
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.shape = createQuad([0, 0, 0], 0.0, 0.0)

# Funcion para detectar las colisiones entre un objeto y la bola
def Collision (Objeto, Ball):
    # Hacer las colisiones para una lado y para otro no me gusta mucho pero se queda asi por mientras
    collisionX = 0
    # Colision con objetos de la der
    if Objeto.x > 0:
        collisionX = (Ball.x + Ball.sizeX/2 >= Objeto.x - Objeto.sizeX/2)
    # Colision con los objetos de la izq 
    else:
        collisionX = (Ball.x - Ball.sizeX/2 <= Objeto.x + Objeto.sizeX/2) 
    collisionY = Ball.y <= Objeto.y + Objeto.sizeY/2 and Ball.y >= Objeto.y - Objeto.sizeY/2
    return collisionX and collisionY

# Calcula la diferencia entre dos puntos
# Usada para que cuando la bola choca con los extremos aumente su velocidad
def diferencia (y1 , y0):
    dif = np.abs( y1 - y0)
    return dif

# Funcion que imprime uwu's
# se supone que iba a reiniciar el juego
def reiniciarJuego ():
    print("uwu")


# Initialize glfw
if not glfw.init():
    sys.exit()

width = 800
height = 500

window = glfw.create_window(width, height, "pong", None, None)

if not window:
    glfw.terminate()
    sys.exit()

glfw.make_context_current(window)

# Connecting the callback function 'on_key' to handle keyboard events
glfw.set_key_callback(window, on_key)
# Assembling the shader program (pipeline) with both shaders
pipeline = es.SimpleTransformShaderProgram()

# Defining shaders for our pipeline
vertex_shader = """
#version 130
in vec3 position;
in vec3 color;

out vec3 fragColor;

uniform mat4 transform;

void main()
{
    fragColor = color;
    gl_Position = transform * vec4(position, 1.0f);
}
"""

fragment_shader = """
#version 130

in vec3 fragColor;
out vec4 outColor;

void main()
{
    outColor = vec4(fragColor, 1.0f);
}
"""

# Assembling the shader program (pipeline) with both shaders
shaderProgram = OpenGL.GL.shaders.compileProgram(
    OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
    OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

# Telling OpenGL to use our shader program
glUseProgram(shaderProgram)
# Telling OpenGL to use our shader program
glUseProgram(pipeline.shaderProgram)

# Setting up the clear screen color
glClearColor(0.0, 0.0, 0.0, 1.0)

# Creating shapes on GPU memory
lines = createLines(7)
numbers = nr.createNumbers()

# Iniciar jugadores
j1 = Player(0.9, 0)
j2 = Player(-0.9, 0)

# Mapa
# Muros invisibles que detectan las colisiones laterales
muroDerecho = Rectangulo(0.98, 0.0, 0.05, 2.0)
muroIzquierdo = Rectangulo(-0.98, 0.0, 0.05, 2.0)

# Se inicia la bola
ball = Ball()

# Fill mode Polygon
glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

# Get initial time
t0 = 0

# Contados de los puntos
puntos_j1 = 0
puntos_j2 = 0

# Como arriba y abajo no hay muros, aqui estan las variables para
# que no colisione dos veces en el mismo lado
colision_sup = False
colision_inf = False


# Coleccion de los numeros que se usan para el puntaje
coleccion_numeros = [nr.createCero(), nr.createUno(), nr.createDos(), nr.createTres()]

while not glfw.window_should_close(window):

    if puntos_j1 != 3 and puntos_j2 != 3:

        # Nodos de los puntajes que se muestran en pantalla
        nodo_puntaje_j1 = sg.findNode(numbers, "scaledNumber1")
        nodo_puntaje_j2 = sg.findNode(numbers, "scaledNumber0")

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0

        # xf = x0 + vx*dt
        # yf = x0 + vy*dt
        desplazamientoX = ball.x_collision + dt * ball.vX 
        desplazamientoY = ball.y_collision + dt * ball.vY

        ball.x = desplazamientoX
        ball.y = desplazamientoY

        # Colisiones Superiores e inferiores
        if np.abs(ball.y) > 0.95:
            ball.x_collision = ball.x
            ball.y_collision = ball.y
            ball.vY = -ball.vY
            t0 = t1
            # Esto es para que no colisione en el mismo lugar mas de 1 vez
            if ball.x > 0 and colision_sup == False:
                colision_sup = True
                colision_inf = False
            elif ball.x <  0 and colision_inf == False:
                colision_inf = True
                colision_sup = False
        # Colisiones dentro de la cancha
        elif np.abs(ball.x) < j1.x + j1.sizeX/2:
            # Colision con J1
            if Collision(j1, ball) and j1.aColisionado == False:
                j1.aColisionado = True
                j2.aColisionado = False
                ball.x_collision = ball.x
                ball.y_collision = ball.y
                ball.vX = -ball.vX
                t0 = t1

                # Esto le da direccion a la bola dependiendo del sentido en que se mueve j1
                if (j1.direccion == False and ball.vY > 0) or (j1.direccion == True and ball.vY <0):
                    ball.vY = -ball.vY

                dif = diferencia(ball.y, j1.y)
                # Mayor velocidad si colisiona en el extremo del jugador
                if dif > 0.1875:
                    ball.vX = ball.vX * 1.4
                elif dif <  0.03:
                    ball.vX = ball.vX * 0.95
            # Colision con j2
            elif Collision(j2, ball) and j2.aColisionado == False:
                j2.aColisionado = True
                j1.aColisionado = False
                ball.x_collision = ball.x
                ball.y_collision = ball.y
                ball.vX = -ball.vX
                t0 = t1

                # Esto le da direccion a la bola dependiendo del sentido en que se mueve j2
                if (j2.direccion == False and ball.vY > 0) or (j2.direccion == True and ball.vY <0):
                    ball.vY = -ball.vY

                dif = diferencia(ball.y, j2.y)
                # Si hay colision con el extremo del j2 entonces la bola ira mas rapido
                if dif > 0.1875: # 3/4 de 0.25= sizeY /2s
                    ball.vX = ball.vX * 1.4
                elif dif <  0.03:
                    ball.vX = ball.vX * 0.95

        # Colision con el lado derecho de la ventana
        elif Collision(muroDerecho, ball):
            t0 = 0
            ball.reset()
            ball.vX = -ball.vX
            ball.vY = -ball.vY
            j1.reset()
            j2.reset()
            puntos_j2 += 1
            nodo_puntaje_j2.childs = [coleccion_numeros[puntos_j2]]

        # Colision con el lado izquierdo de la ventana
        elif Collision(muroIzquierdo,ball):
            t0 = 0
            ball.reset()
            j1.reset()
            j2.reset()
            puntos_j1 += 1
            nodo_puntaje_j1.childs = [coleccion_numeros[puntos_j1]]

    # Using GLFW to check for input events
    glfw.poll_events()

    # Filling or not the shapes depending on the controller state
    if controller.fillPolygon:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Clearing the screen in both, color and depth
    glClear(GL_COLOR_BUFFER_BIT)

    # Create transform matrix
    # Transform de J1
    transform = tr.matmul([
        tr.translate(j1.x, j1.y, 0),
        tr.scale(j1.sizeX, j1.sizeY, 1)
    ])

    # Transform de j2
    transform2 = tr.matmul([
        tr.translate(j2.x, j2.y, 0),
        tr.scale(j2.sizeX, j2.sizeY, 1)
    ])

    # Transform de la bola
    transformBall = tr.matmul([
        tr.translate(ball.x, ball.y, 0),
        tr.scale(ball.sizeX, ball.size, 1)
    ])

    # Transform del muro invisible derecho
    transformMuroDerecho = tr.matmul([
        tr.translate(muroDerecho.x, muroDerecho.y, 0),
        tr.scale(muroDerecho.sizeX, muroDerecho.sizeY, 1)
    ])

    # Transform del muro invisible izquierdo
    transformMuroIzquierdo = tr.matmul([
        tr.translate(muroIzquierdo.x, muroIzquierdo.y, 0),
        tr.scale(muroIzquierdo.sizeX, muroIzquierdo.sizeY, 1)
    ])

    # Drawing the Lines
    sg.drawSceneGraphNode(lines, pipeline, "transform")
    sg.drawSceneGraphNode(numbers, pipeline, "transform")


    # Drawing the Quad with the given transformation
    drawShape(shaderProgram, j1.shape, transform)
    drawShape(shaderProgram, j2.shape, transform2)
    drawShape(shaderProgram, ball.shape, transformBall)
    drawShape(shaderProgram, muroDerecho.shape, transformMuroDerecho)
    drawShape(shaderProgram, muroIzquierdo.shape, transformMuroIzquierdo)


    # Once the render is done, buffers are swapped, showing only the complete scene.
    glfw.swap_buffers(window)

glfw.terminate()




