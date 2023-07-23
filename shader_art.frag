#version 440

// in float width;
// in float height;

out vec4 outColor;

void main() {

    float x0 = (gl_FragCoord.x/1920.0) * 2.47 - 2.0;
    float y0 = (gl_FragCoord.y/1080.0) * 2.24 - 1.12;
    
    float xtemp;
    float x = 0.0;
    float y = 0.0;
    int iteration = 0;
    int max_iterations = 1000;
    while (x*x + y*y <= 4 && iteration < max_iterations) {
        xtemp = x*x - y*y + x0;
        y = 2*x*y + y0;
        x = xtemp;
        iteration = iteration + 1;
    }
    outColor = vec4(iteration % 2, 0.0, (iteration % 2) + 1.0, 1.0);
/*
    if(iteration <= 100)
        outColor = vec4(0.1, 0.0, 0.0, 1.0);
    else if(iteration <= 200)
        outColor = vec4(0.1, 0.1, 0.0, 1.0);
    else if(iteration <= 300)
        outColor = vec4(0.1, 0.1, 0.1, 1.0);
    else if(iteration <= 400)
        outColor = vec4(0.3, 0.1, 0.1, 1.0);
    else if(iteration <= 500)
        outColor = vec4(0.3, 0.3, 0.1, 1.0);
    else if(iteration <= 600)
        outColor = vec4(0.3, 0.3, 0.3, 1.0);
    else if(iteration <= 700)
        outColor = vec4(0.6, 0.3, 0.3, 1.0);
    else if(iteration <= 800)
        outColor = vec4(0.6, 0.6, 0.3, 1.0);
    else if(iteration <= 900)
        outColor = vec4(0.6, 0.6, 0.6, 1.0);
    else 
        outColor = vec4(0.9, 0.6, 0.6, 1.0);
*/
}
