	xy = featureMapThisCorrdinate + vec2({fThisX}, {fThisY});
	tmp = weights[{idx} + {align}] * texture2D(featureMapThis, xy);
	{param} += tmp.r;
	{param} += tmp.g;
	{param} += tmp.b;
	{param} += tmp.a;
