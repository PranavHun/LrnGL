import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import pyrr
from PIL import Image
import time 

xmov = 0.0
ymov = 0.0
dxmov = 0.05
rotation = 0


def key_callback_func(window, key, scancode, action, mods):
    global xmov, dxmov, ymov, rotation
    # print(f"{key} {action}")

    if key == glfw.KEY_CAPS_LOCK and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)
    if key == glfw.KEY_A and (action == glfw.PRESS or action == glfw.REPEAT):
        xmov -= dxmov
    if key == glfw.KEY_D and (action == glfw.PRESS or action == glfw.REPEAT):
        xmov += dxmov
    if key == glfw.KEY_W and (action == glfw.PRESS or action == glfw.REPEAT):
        ymov += dxmov
    if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):
        ymov -= dxmov
    if key == glfw.KEY_LEFT and (action == glfw.PRESS or action == glfw.REPEAT):
        rotation = rotation - 1 if rotation > -35 else -35
    if key == glfw.KEY_RIGHT and (action == glfw.PRESS or action == glfw.REPEAT):
        rotation = rotation + 1 if rotation < 35 else 35

def create_transform_mat (translate_x, translate_y, translate_z, rotate_x, rotate_y, rotate_z, scale_x, scale_y, scale_z):
    transform_mat = pyrr.Matrix44.identity()
    transform_mat = transform_mat * pyrr.matrix44.create_from_translation(np.array([translate_x, translate_y, translate_z]))
    transform_mat = transform_mat * pyrr.matrix44.create_from_x_rotation(np.deg2rad(rotate_x))
    transform_mat = transform_mat * pyrr.matrix44.create_from_y_rotation(np.deg2rad(rotate_y))
    transform_mat = transform_mat * pyrr.matrix44.create_from_z_rotation(np.deg2rad(rotate_z))
    transform_mat = transform_mat * pyrr.matrix44.create_from_scale(np.array([scale_x, scale_y, scale_z]))
    return transform_mat

def main():
    if not glfw.init():
        return

    window = glfw.create_window(1920, 1080, "Pyopengl Texturing Cube", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    
    cube = [-0.5, -0.5, 0.0,
             0.5, -0.5, 0.0,
             0.0, 0.5, 0.0
        ]
# convert to 32bit float

    cube = np.array(cube, dtype=np.float32)
    indices = [0, 1, 2]
    indices = np.array(indices, dtype=np.uint32)

    VERTEX_SHADER = open("shader.vert").read()
    FRAGMENT_SHADER = open("shader.frag").read()
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

    glUseProgram(shader)

    glClearColor(0.0, 0.0, 0.5, 1.0)
    glEnable(GL_DEPTH_TEST)

    projection = pyrr.Matrix44.identity() * pyrr.matrix44.create_perspective_projection(45.0, 1920.0 / 1080.0, 0.1, 100.0)
    view_matrix = pyrr.matrix44.create_look_at(
        pyrr.vector3.create(0, 0.0, 1), #camera position
        pyrr.vector3.create(0, 0, 0), #camera target
        pyrr.vector3.create(0, 1, 0)  #camera up vector
        )
    
    ypos = ((np.random.random(100) - 0.5) / 3.0)

    WAIT_TIME = 1000.0 / 60.0
    frame_start = time.time()
    ywav = 0

    glfw.set_key_callback(window, key_callback_func)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        transformLoc = glGetUniformLocation(shader, "transform")

        for i in range(100):
            camera_transform_mat = create_transform_mat(0.0, 0.0, 0.0, 0.0, rotation, 0.0, 1.0, 1.0, 1.0)
            perspective = projection * camera_transform_mat * view_matrix
            transform_mat = create_transform_mat(-0.5+xmov+dxmov, ypos[i]+ymov+np.sin(np.deg2rad(10*(i+ywav))), -i, 0.0, -i*45.0/100, 0.0, 0.5, 0.5, 0.5)
            transform_mat_global = create_transform_mat(0.0, 0.0, 0.0, 0.0, -i*45.0/100.0, 0.0, 1.0, 1.0, 1.0)
            glUniformMatrix4fv(transformLoc, 1, GL_FALSE, perspective * transform_mat_global * transform_mat)
            glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)

            transform_mat = create_transform_mat(0.5+xmov+dxmov, ypos[i]+ymov+np.cos(np.deg2rad(10*(i+ywav))), -i, 0.0, i*45.0/100, 0.0, 0.5, 0.5, 0.5)
            transform_mat_global = create_transform_mat(0.0, 0.0, 0.0, 0.0, i*45.0/100.0, 0.0, 1.0, 1.0, 1.0)
            glUniformMatrix4fv(transformLoc, 1, GL_FALSE, perspective * transform_mat_global * transform_mat)
            glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)
        if(time.time() - frame_start) < WAIT_TIME:
            duration = (WAIT_TIME - (time.time() - frame_start))
            time.sleep(duration / 1000.0)
        frame_start = time.time()
        ywav = (ywav + 1) % 260

    glfw.terminate()


if __name__ == "__main__":
    main()
