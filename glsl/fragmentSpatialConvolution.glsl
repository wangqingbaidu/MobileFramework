#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
precision highp int;
#else
precision mediump float;
precision mediump int;
#endif
varying highp vec2 textureCoordinate;
uniform sampler2D featureMapThis;
//Every time it needs to be overwrite.
uniform sampler2D featureMapOut;
//weights_num is kW * kH * 4
uniform vec4 weights[{weights_num}];
//bias divided into n parts
uniform vec4 biases;
uniform bool activated;

float sum_weight(vec4 c) {{
   return c.r + c.g + c.b + c.a;
}}

vec4 ef(vec4 in_color)
{{
	return (in_color + 128.0) / 255.0;
}}

vec4 df(vec4 in_color)
{{
	return in_color * 255.0 - 128.0;
}}

void main()
{{
	vec2 xy;
	vec4 mat_mul;
	vec4 color_this;
	vec4 tmp = vec4(biases);
	vec4 feature_map_out = texture2D(featureMapOut, textureCoordinate.xy);
{loop_weights}

	//If activation activation = clamp(step(0, tmp + feature_map_out) + vec4(`leaky_slope`), 0.0, 1.0);
	if (activated)
	{{
		vec4  activation = clamp(step(0.0, tmp + feature_map_out) + vec4({leaky_slope}), 0.0, 1.0);
		gl_FragColor = (tmp + feature_map_out) * activation;
	}}
	else
	{{
		gl_FragColor = ef(tmp + feature_map_out);
	}}
}}
