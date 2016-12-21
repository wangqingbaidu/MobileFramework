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
{
	gl_FragColor = texture2D(featureMapThis, textureCoordinate.xy);
}
