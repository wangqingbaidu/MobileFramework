	//Clamp act as padding.
	xy = clamp(textureCoordinate + vec2({x_align}, {y_align}), 0.0, 1.0);
	mat_mul = weights[idx] * texture2D(featureMapThis, xy);
	tmp.{c} += mat_mul.r;
	tmp.{c} += mat_mul.g;
	tmp.{c} += mat_mul.b;
	tmp.{c} += mat_mul.a;
