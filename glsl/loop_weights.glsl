	//Clamp act as padding.
	xy = clamp(textureCoordinate + vec2({x_align}, {y_align}), 0.0, 1.0);
	color_this = texture2D(featureMapThis, xy);
	mat_mul = weights[{kSize} * 0 + {idx}] * color_this;
	tmp.r += sum_weight(mat_mul);
	mat_mul = weights[{kSize} * 1 + {idx}] * color_this;
	tmp.g += sum_weight(mat_mul);
	mat_mul = weights[{kSize} * 2 + {idx}] * color_this;
	tmp.b += sum_weight(mat_mul);
	mat_mul = weights[{kSize} * 3 + {idx}] * color_this;
	tmp.a += sum_weight(mat_mul);
