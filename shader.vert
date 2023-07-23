#version 440

layout (location = 0) in vec3 position;
out vec3 newColor;
uniform mat4 transform; 

void main() {
    vec4 pos = transform * vec4(position, 1.0f);
    gl_Position = pos;
    newColor = vec3(1.0f, 1.0f, 1.0f); // / abs(pos.z);
}
