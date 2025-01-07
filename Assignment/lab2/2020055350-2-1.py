import glfw
from OpenGL.GL import *
import numpy as np

arr = [GL_POLYGON,GL_POINTS,GL_LINES,GL_LINE_STRIP,GL_LINE_LOOP,GL_TRIANGLES,GL_TRIANGLE_STRIP,GL_TRIANGLE_FAN,GL_QUADS,GL_QUAD_STRIP]
a = GL_LINE_LOOP
def render ():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(a)
    x = np.linspace(0,2*np.pi,12,False)
    for i in range (0,12):
        glVertex2f(np.cos(x[i]), np.sin(x[i]))
    glEnd()
    return

def key_callback(window , key, scancode, action, mods):
    if action==glfw.PRESS:
        if(glfw.KEY_0<=key<=glfw.KEY_9):
            global a
            a = arr[key-glfw.KEY_0]
        return
        
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2020055350-2-1",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__=="__main__":
    main()