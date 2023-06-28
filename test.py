import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluPerspective

PIT_WIDTH = 100
PADDING = 20
BOARD_WIDTH = 8 * PIT_WIDTH + 9 * PADDING

# Colors
computer = (250/255, 246/255, 246/255)
player = (105/255, 53/255, 63/255)

# Initialize Pygame
pygame.init()
pygame.display.set_caption('3D Mancala Board')
pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 16)
screen = pygame.display.set_mode((BOARD_WIDTH, 600), DOUBLEBUF | OPENGL)

# Set up OpenGL
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glEnable(GL_DEPTH_TEST)

# Set up camera
gluPerspective(45, (BOARD_WIDTH / 600), 0.1, 50)
glTranslatef(0, -175, -450)
glRotatef(25, 1, 0, 0)


def draw_cube(x, y, z, width, color):
    vertices = [
        [x, y, z],
        [x + width, y, z],
        [x + width, y + width, z],
        [x, y + width, z],
        [x, y, z + width],
        [x + width, y, z + width],
        [x + width, y + width, z + width],
        [x, y + width, z + width],
    ]
    edges = (
        (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)
    )
    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [2, 3, 7, 6],
        [0, 3, 7, 4],
        [1, 2, 6, 5],
    ]
    glBegin(GL_QUADS)
    for face in faces:
        glColor3f(*color)
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_board():
    for i in range(1, 7):
        x = i * (PIT_WIDTH + PADDING)
        draw_cube(x, 160, 0, PIT_WIDTH, computer)
        draw_cube(x, 300, 0, PIT_WIDTH, player)

    draw_cube(PADDING, 160, 0, 100, computer)
    draw_cube(7 * PIT_WIDTH + 8 * PADDING, 160, 0, 100, player)

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        if event.type == VIDEORESIZE:
            width, height = event.size
            pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
            glViewport(0, 0, width, height)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_board()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()