import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import pyrr
from PIL import Image

def projection():
    scale_matrix = pyrr.matrix44.create_from_scale([1, 1, 1])
    rot_matrix = pyrr.Matrix44.identity()
    trans_matrix = pyrr.matrix44.create_from_translation([0, 0, -5])

    model_matrix = scale_matrix * rot_matrix * trans_matrix
    view_matrix = pyrr.matrix44.create_look_at(np.array([4, 3, 3]), np.array([1, 1, 0]), np.array([0, 1, 0]))
    proj_matrix = pyrr.matrix44.create_perspective_projection_matrix(45.0, 1920.0/1080.0, 0.1, 1000.0)
    mvp_matrix = proj_matrix * view_matrix * model_matrix
    #mvp_matrix = view_matrix * model_matrix

    return mvp_matrix

def main():
    if not glfw.init():
        return

    window = glfw.create_window(1920, 1080, "Pyopengl Texturing Cube", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)



    #        positions         colors          texture coords
    cube = [-0.5, -0.5, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.5, -0.5, 0, 0.0, 0.0, 0.0, 1.0, 0.0,
             0.5,  0.5, 0, 0.0, 0.0, 0.0, 0.5, 1.0]
    


# convert to 32bit float

    cube = np.array(cube, dtype=np.float32)

    indices = [0, 1, 2]

    indices = np.array(indices, dtype=np.uint32)



    VERTEX_SHADER = """

              #version 330

              layout (location = 0) in vec3 position;

              layout (location = 1) in vec3 Incolor;
              layout (location = 2) in vec2 InTexCoords;

              out vec3 newColor;
              out vec2 OutTexCoords;
              
              uniform mat4 transform; 

              void main() {
               gl_Position = transform * vec4(position, 1.0f);
               newColor = Incolor;
               OutTexCoords = InTexCoords;

                }


          """

    FRAGMENT_SHADER = """
           #version 330

            in vec3 newColor;
            in vec2 OutTexCoords;

            out vec4 outColor;
            uniform sampler2D samplerTex;

           void main() {

              outColor = vec4(newColor, 1.0) + texture(samplerTex, OutTexCoords);

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
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)



    # get the color from  shader
    color = glGetAttribLocation(shader, 'Incolor')
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 8, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)


    texCoords = glGetAttribLocation(shader, "InTexCoords")
    print(f"{position}, {color}, {texCoords}")

    glVertexAttribPointer(texCoords, 2, GL_FLOAT, GL_FALSE,  cube.itemsize * 8, ctypes.c_void_p(24))
    glEnableVertexAttribArray(texCoords)

    

    #Texture Creation
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    image = Image.open("wood.jpg")
    img_data = np.array(list(image.getdata()), np.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glEnable(GL_TEXTURE_2D)

    glUseProgram(shader)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    rot_z = pyrr.Matrix44.from_z_rotation(1)
    scale_x = pyrr.Matrix44.from_scale([(1080.0 / 1920.0), 1, 1])
    translate_x = pyrr.Matrix44.from_translation([-5, -5, -1])
    perspective = pyrr.matrix44.create_perspective_projection_matrix(50.0, 1920.0/1080.0, 5, 1000.0)
    transform_mat = np.matmul(scale_x * rot_z * translate_x, perspective)
    print(perspective)
    print("\n")
    print(scale_x * rot_z * translate_x)
    print("\n")
    print(np.matmul(scale_x * rot_z * translate_x, perspective))


    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        transformLoc = glGetUniformLocation(shader, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, transform_mat)

        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)
       

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
