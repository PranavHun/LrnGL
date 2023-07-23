import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import pyrr
from PIL import Image
import time 


def key_callback_func(window, key, scancode, action, mods):
    global xmov, dxmov, ymov, rotation
    # print(f"{key} {action}")

    if key == glfw.KEY_CAPS_LOCK and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)

def canvas():
    cube = [-1.0, -1.0, 0.0,
            1.0, -1.0, 0.0,
            -1.0, 1.0, 0.0,
            1.0, 1.0, 0.0
    ]
    # convert to 32bit float
    cube = np.array(cube, dtype=np.float32)
    indices = [0, 1, 2, 3]
    indices = np.array(indices, dtype=np.uint32)

    VERTEX_SHADER = open("shader_art.vert").read()
    FRAGMENT_SHADER = open("shader_art.frag").read()
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER))


    # Create Buffer object in gpu
    VBO = glGenBuffers(1)
    # Bind the buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, cube.itemsize * len(cube), cube, GL_STATIC_DRAW)

    # Create EBO
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)


    # get the position from  shader
    position = glGetAttribLocation(shader, 'position')
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    return shader


def main():
    if not glfw.init():
        return

    window = glfw.create_window(1920, 1080, "Shader Art", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    shader = canvas()
    glUseProgram(shader)
     


    # glClearColor(0.0, 0.0, 0.5, 1.0)
    WAIT_TIME = 1000.0 / 60.0
    frame_start = time.time()

    glfw.set_key_callback(window, key_callback_func)
    # transformLoc = glGetUniformLocation(shader, "screen_resolution")
    # resolution = pyrr.Vector3([1920, 1080, 0])
    # glUniform3fv(transformLoc, 1, resolution)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glDrawElements(GL_TRIANGLE_STRIP, 4, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)
        if(time.time() - frame_start) < WAIT_TIME:
            duration = (WAIT_TIME - (time.time() - frame_start))
            time.sleep(duration / 1000.0)
        frame_start = time.time()

    glfw.terminate()


if __name__ == "__main__":
    main()
