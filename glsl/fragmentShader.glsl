#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
precision highp int;
#else
precision mediump float;
precision mediump int;
#endif
varying highp vec2 textureCoordinate;
uniform sampler2D featureMapThis;
uniform sampler2D featureMapOut;
uniform float weights[{weights_num}];
uniform float biases[{biases_num}];

void main()
{{
	vec4 out = texture2D(featureMapOut, textureCoordinate.xy);
	vec4 tmp;
	vec2 xy;
	//textureCoordinate.x % 1/width
	vec2 featureMapThisCorrdinate = vec2(textureCoordinate.x % (1.0 / {blockX}), textureCoordinate.y % (1.0 / {blockY}));
	featureMapThisCorrdinate *= vec2({dW}, {dH});
	int weights_idx = floor(textureCoordinate.x * {blockX}) + floor(textureCoordinate.y * {blockY}) * {blockX};
{if_conditions}
	weights_idx = weights_idx * 4;
{loop_biases}
	weights_idx = weights_idx * {kW} * {kH};
{loop_weights}
	gl_FragColor = out;
}}
