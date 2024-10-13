# importing opengl stuff (its tricky but let's try!)
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *


class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.mri_data = None  # init mri_data (has 2 be set later)
        self.angle = 0  # rotate? sure why not

    def set_mri_data(self, data):
        # sets mri and triggers redrawin (or something)
        self.mri_data = data
        self.update()

    def initializeGL(self):
        # Setup OpenGL settings
        glClearColor(0.0, 0.0, 0.0, 1.0)  # black background
        glEnable(GL_DEPTH_TEST)  # make sure 3d works

        # Set the camera (does this even work?)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, 1, 0.1, 100.0)  # set the perspective
        glMatrixMode(GL_MODELVIEW)

    def resizeGL(self, w, h):
        # Adjust the viewport when the window resizes
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45.0, w / h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        # Clear screen (lets get rid of all the garbage from prev frames!)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.mri_data is not None:
            self.draw_brain()  # draw brain? ye

        # update the view
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)  # camera moves back
        glRotatef(self.angle, 1.0, 1.0, 0.0)  # spinning the brain for some reason?
        self.angle += 1  # slowly rotato brain

        self.swapBuffers()

    def draw_brain(self):
        # draw cubes for now? (brain cubed woohoo lol)
        slices = self.mri_data.shape[2]  # the number of slices
        for z in range(slices):
            glBegin(GL_QUADS)  # Drawing a 2D plane for each MRI slice
            for x in range(self.mri_data.shape[0]):
                for y in range(self.mri_data.shape[1]):
                    intensity = self.mri_data[x, y, z] / np.max(self.mri_data)
                    glColor3f(intensity, intensity, intensity)  # grayscale
                    # draw a simple cubelet
                    glVertex3f(x / slices, y / slices, z / slices)
                    glVertex3f((x + 1) / slices, y / slices, z / slices)
                    glVertex3f((x + 1) / slices, (y + 1) / slices, z / slices)
                    glVertex3f(x / slices, (y + 1) / slices, z / slices)
            glEnd()
