#version 300 es

// Vertex shader for galaxy point rendering
precision highp float;

in vec3 aPosition;
in float aMagnitude;
in vec3 aColor;

uniform mat4 uModelViewMatrix;
uniform mat4 uProjectionMatrix;
uniform float uPointSize;
uniform float uDistanceScale;

out float vMagnitude;
out vec3 vColor;

void main() {
    // Transform vertex position
    vec4 worldPos = uModelViewMatrix * vec4(aPosition, 1.0);
    gl_Position = uProjectionMatrix * worldPos;
    
    // Calculate point size based on distance and magnitude
    float distance = length(worldPos.xyz);
    float sizeFactor = uPointSize * (1.0 + aMagnitude * 0.1);
    gl_PointSize = sizeFactor * uDistanceScale / distance;
    
    // Ensure minimum point size for visibility
    gl_PointSize = max(gl_PointSize, 1.0);
    
    // Pass attributes to fragment shader
    vMagnitude = aMagnitude;
    vColor = aColor;
}