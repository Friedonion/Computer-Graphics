import glfw
from OpenGL.GL import *
import numpy as np

T = np.identity(3,dtype=float)

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

def key_callback(window , key, scancode, action, mods):
    if action==glfw.PRESS:
        s = np.sin(np.deg2rad(10))
        c = np.cos(np.deg2rad(10))
        global T
        if(key == glfw.KEY_Q):
            T = np.array([[1,0,-0.1],[0,1,0],[0,0,1]])@T
        if(key == glfw.KEY_E):
            T = np.array([[1,0,0.1],[0,1,0],[0,0,1]])@T
        if(key == glfw.KEY_D):
            T = T@np.array([[c,s,0],[-s,c,0],[0,0,1]])
        if(key == glfw.KEY_A):
            T = T@np.array([[c,-s,0],[s,c,0],[0,0,1]])
        if(key == glfw.KEY_1):
            T = np.identity(3,dtype=float)
        return

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2020055350-3-1",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(T)
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__=="__main__":
    main()