import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import pyrr
from PIL import Image
import time

global viewport_changed


def reshape_callback_func(window, w, h):
    global viewport_changed
    viewport_changed = True


def key_callback_func(window, key, scancode, action, mods):
    global xmov, dxmov, ymov, rotation, zoom, dzoom, pan_x, pan_y, dpan
    # print(f"{key} {action}")

    if (key == glfw.KEY_ESCAPE or key == glfw.KEY_Q) and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)


def canvas():
    canvas = np.array([-1.0, -1.0, 0.0,
                       1.0, -1.0, 0.0,
                       -1.0, 1.0, 0.0,
                       1.0, 1.0, 0.0
                       ], dtype=np.float32)

    VERTEX_SHADER = """
    #version 440
    layout (location = 0) in vec3 position;
    void main() {
        gl_Position = vec4(position, 1.0);
    }"""
    open("sample.frag", "r").read()
    FRAGMENT_SHADER = """
    #version 440
    
    uniform vec2 ScreenSize;
    uniform uint FrameNo;
    out vec4 outColor;
    
    """ + open("sample.frag", "r").read() + """

    void main() {
        outColor = draw_canvas();
    }"""

    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER))

    # Create Buffer object in gpu
    VBO = glGenBuffers(1)
    # Bind the buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, canvas.itemsize *
                 len(canvas), canvas, GL_STATIC_DRAW)

    # get the position from  shader
    position = glGetAttribLocation(shader, 'position')
    glVertexAttribPointer(position, 3, GL_FLOAT,
                          GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    return shader


def main():
    if not glfw.init():
        return

    window = glfw.create_window(1000, 1000, "Shader Art", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    shader = canvas()
    glUseProgram(shader)

    # glClearColor(0.0, 0.0, 0.5, 1.0)
    WAIT_TIME = 1000.0 / 60.0
    frame_start = time.time()
    frame_number = 0
    global viewport_changed
    viewport_changed = False

    screen_size_loc = glGetUniformLocation(shader, "ScreenSize")
    w, h = glfw.get_framebuffer_size(window)
    glViewport(0, 0, w, h)
    glUniform2fv(screen_size_loc, 1, np.array(
        [w, h], dtype=np.float32))

    glfw.set_key_callback(window, key_callback_func)
    glfw.set_window_size_callback(window, reshape_callback_func)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        frame_number_loc = glGetUniformLocation(shader, "FrameNo")
        glUniform1ui(frame_number_loc, frame_number)

        if viewport_changed:
            viewport_changed = False
            w, h = glfw.get_framebuffer_size(window)
            glViewport(0, 0, w, h)
            glUniform2fv(screen_size_loc, 1, np.array(
                [w, h], dtype=np.float32))

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        glfw.swap_buffers(window)
        frame_number = frame_number + 1 if frame_number < 360 else 0
        if (time.time() - frame_start) < WAIT_TIME:
            duration = (WAIT_TIME - (time.time() - frame_start))
            time.sleep(duration / 1000.0)
        frame_start = time.time()

    glfw.terminate()


if __name__ == "__main__":
    main()
