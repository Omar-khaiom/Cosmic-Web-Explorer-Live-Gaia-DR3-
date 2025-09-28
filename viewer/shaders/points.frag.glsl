#version 300 es

// Fragment shader for galaxy point rendering
precision highp float;

in float vMagnitude;
in vec3 vColor;

uniform float uAlpha;
uniform float uBrightnessFactor;

out vec4 fragColor;

void main() {
    // Calculate distance from center of point
    vec2 coord = gl_PointCoord - vec2(0.5);
    float dist = length(coord);
    
    // Create circular points with smooth falloff
    float alpha = 1.0 - smoothstep(0.0, 0.5, dist);
    alpha *= uAlpha;
    
    // Adjust brightness based on magnitude
    float brightness = uBrightnessFactor * (1.0 - vMagnitude * 0.1);
    vec3 finalColor = vColor * brightness;
    
    // Add some glow effect for brighter stars
    if (vMagnitude < 0.5) {
        finalColor += vec3(0.2, 0.2, 0.3) * (0.5 - vMagnitude);
    }
    
    fragColor = vec4(finalColor, alpha);
}