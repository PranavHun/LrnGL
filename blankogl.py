import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import pyrr
from PIL import Image
import time 

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

    VERTEX_SHADER = """

              #version 440

              layout (location = 0) in vec3 position;

              out vec3 newColor;
              
              uniform mat4 transform; 

              void main() {

                vec4 pos = transform * vec4(position, 1.0f);

               gl_Position = pos;
               newColor = vec3(1.0f, 1.0f, 1.0f) / abs(pos.z * pos.z);
              }



          """

    FRAGMENT_SHADER = """
           #version 330

            in vec3 newColor;

            out vec4 outColor;

           void main() {
              outColor = vec4(newColor, 1.0);
            }

       """



    # Compile The Program and shaders

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
    view_matrix = pyrr.Matrix44.identity() * pyrr.matrix44.create_look_at(
        pyrr.vector3.create(0, 0.4, 1), #camera position
        pyrr.vector3.create(0, 0, 0), #camera target
        pyrr.vector3.create(0, 1, 0)  #camera up vector
        )
    perspective = projection * view_matrix
    print(perspective * create_transform_mat(0.5, 0.0, 0.0, 45, 0 , 0, 0.5, 0.5, 0.5))
    rotation = 0
    xmov = 0.0
    dxmov = 0.05

    WAIT_TIME = 1000.0 / 60.0
    frame_start = time.time()
    
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        transformLoc = glGetUniformLocation(shader, "transform")

        for i in range(100):
            transform_mat = create_transform_mat(-0.5+xmov+dxmov, 0.0, -i, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5)
            # transform_mat_global = create_transform_mat(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0)
            glUniformMatrix4fv(transformLoc, 1, GL_FALSE, perspective * transform_mat)
            glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)

            transform_mat = create_transform_mat(0.5+xmov+dxmov, 0.0, -i, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5)
            # transform_mat_global = create_transform_mat(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0)
            glUniformMatrix4fv(transformLoc, 1, GL_FALSE, perspective * transform_mat)
            glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)

        rotation = 0 if rotation == 360 else rotation + 1
        dxmov = -dxmov if xmov >= 1.0 or xmov <= -1.0 else dxmov
        xmov += dxmov

        glfw.swap_buffers(window)
        if(time.time() - frame_start) < WAIT_TIME:
            duration = (WAIT_TIME - (time.time() - frame_start))
            time.sleep(duration / 1000.0)
        frame_start = time.time()


    glfw.terminate()


if __name__ == "__main__":
    main()
