import glfw
from OpenGL.GL import *
import numpy as np


def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cordinate
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0,255,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    #draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255,255,255)
    glVertex2fv((T @ np.array([.0,.5,1.]))[:-1])
    glVertex2fv((T @ np.array([.0,.0,1.]))[:-1])
    glVertex2fv((T @ np.array([.5,.0,1.]))[:-1])
    glEnd()

        
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2020055350-2-2",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        t = glfw.get_time()
        s = np.sin(t)
        c = np.cos(t)
        T= np.identity(3,dtype=float)
        T = np.array([[c,-s,0],[s,c,0],[0,0,1]])
        K= np.identity(3,dtype=float)
        K = np.array([[1,0,0.5],[0,1,0],[0,0,1]])
        T=T@K
        render(T)
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__=="__main__":
    main()