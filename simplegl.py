import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import pyrr

def main():
    if not glfw.init():
        return

    window = glfw.create_window(1920, 1080, "Pyopengl Texturing Cube", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)



    #        positions         colors
    cube = [-0.5, -0.5, 0, 1.0, 0.0, 0.0,
                 0.5, -0.5, 0, 0.0, 1.0, 0.0,
                 0.5,  0.5, 0, 0.0, 0.0, 1.0]
    


# convert to 32bit float

    cube = np.array(cube, dtype=np.float32)

    indices = [0, 1, 2]

    indices = np.array(indices, dtype=np.uint32)



    VERTEX_SHADER = """

              #version 330

              layout (location = 0) in vec3 position;

              layout (location = 1) in vec3 Incolor;

              out vec3 newColor;
              
              uniform mat4 transform; 

              void main() {
               gl_Position = transform * vec4(position, 1.0f);
               newColor = Incolor;
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
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 6, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)



    # get the color from  shader
    color = glGetAttribLocation(shader, 'Incolor')
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 6, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    glUseProgram(shader)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    rot_z = pyrr.Matrix44.from_z_rotation(0)
    #scale_x = pyrr.Matrix44.from_scale([(1080.0 / 1920.0), 1, 1])
    scale_x = pyrr.Matrix44.from_scale([1, 1, 1, 1])
    translate_x = pyrr.Matrix44.from_translation([0.25, .25, 0])
    fov = 60
    aspect_ratio = 800 / 600 #width / height
    near_clip = 0.1
    far_clip = 100

    #create a perspective matrix
    projection_matrix = pyrr.matrix44.create_perspective_projection(
        fov,
        aspect_ratio,
        near_clip,far_clip)
    view_matrix = pyrr.matrix44.create_look_at(pyrr.vector3.create(0, 0, 1), #camera position
pyrr.vector3.create(0, 0, 0), #camera target
pyrr.vector3.create(0, 1, 0)  #camera up vector
)


    transform_mat = np.matmul(np.matmul(np.matmul(scale_x, rot_z), translate_x), np.matmul(projection_matrix, view_matrix))# perspective * scale_x 


    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        transformLoc = glGetUniformLocation(shader, "transform")
        #glUniformMatrix4fv(transformLoc, 1, GL_FALSE, pyrr.Matrix44.identity())
        #glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)

        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, transform_mat)
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)
       

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
