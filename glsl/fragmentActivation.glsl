#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
precision highp int;
#else
precision mediump float;
precision mediump int;
#endif
varying highp vec2 textureCoordinate;
uniform sampler2D featureMapThis;

void main()
{{
	vec4 out = texture2D(featureMapThis, textureCoordinate.xy);
	vec4 activation = clamp(step(0, tmp + feature_map_out) + vec4({leaky_slope}), 0.0, 1.0);
	gl_FragColor = out * act;
}}
