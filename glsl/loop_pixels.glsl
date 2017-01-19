    vec2 c{pixel_index} = textureCoordinate + vec2({x_align}, {y_align});
    vec2 coordinates{pixel_index} = vec2(clamp(c{pixel_index}.x, 0.0000000001, 0.99999999999), clamp(c{pixel_index}.y, 0.0000000001, 0.99999999999));
    vec4 ind{pixel_index} = texture2D(featureMapThis, coordinates{pixel_index});


