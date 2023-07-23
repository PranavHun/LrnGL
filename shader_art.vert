#version 440

layout (location = 0) in vec3 position;
//uniform vec3 screen_resolution;
//out float width;
//out float height;

void main()
{
    //width = screen_resolution.x;
    //height = screen_resolution.y;
    gl_Position = vec4(position, 1.0);
}