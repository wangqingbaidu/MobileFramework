    if (weights_idx * 4 >= biases_num)
    {
        gl_FragColor = vec4(0,0,0,0);
        return;
    }
