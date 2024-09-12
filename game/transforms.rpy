init python:

    renpy.register_shader("example.gradient", variables="""
        uniform vec4 u_gradient_left;
        uniform vec4 u_gradient_right;
        uniform vec2 u_model_size;
        varying float v_gradient_done;
        attribute vec4 a_position;
    """, vertex_300="""
        v_gradient_done = a_position.x / u_model_size.x;
    """, fragment_300="""
        float gradient_done = v_gradient_done;
        gl_FragColor *= mix(u_gradient_left, u_gradient_right, gradient_done);
    """)

    renpy.register_shader("example.gradient_45", variables="""
        uniform vec4 u_gradient_left;
        uniform vec4 u_gradient_right;
        uniform vec2 u_model_size;
        varying float v_gradient_done;
        attribute vec4 a_position;
    """, vertex_300="""
        // Calcula a posição normalizada ao longo da diagonal
        v_gradient_done = (a_position.x + a_position.y) / (u_model_size.x + u_model_size.y);
    """, fragment_300="""
        float gradient_done = v_gradient_done;
        // Interpola a cor entre os dois valores de gradiente
        gl_FragColor *= mix(u_gradient_left, u_gradient_right, gradient_done);
    """)

    renpy.register_shader("example.gradient_with_angle", variables="""
        uniform vec4 u_gradient_left;
        uniform vec4 u_gradient_right;
        uniform vec2 u_model_size;
        uniform float u_angle;
        varying float v_gradient_done;
        attribute vec4 a_position;
    """, vertex_300="""
        // Calcula o vetor direção do gradiente baseado no ângulo
        float cos_angle = cos(u_angle);
        float sin_angle = sin(u_angle);
        
        // Calcula as coordenadas normalizadas
        vec2 normalized_position = a_position.xy / u_model_size;

        // Aplica a rotação ao vetor de direção
        float gradient_direction = normalized_position.y * cos_angle + normalized_position.x * sin_angle;

        v_gradient_done = gradient_direction;
    """, fragment_300="""
        float gradient_done = v_gradient_done;
        // Interpola a cor entre os dois valores de gradiente
        gl_FragColor *= mix(u_gradient_left, u_gradient_right, gradient_done);
    """)


# transform gradient:
#     shader "example.gradient_with_angle"
#     u_gradient_left (0.54, 0.36, 0.64, 1.0)
#     u_gradient_right (0.0, 0.0, 0.0, 0.0)
#     u_angle 3.14159*2/3

#     on hover:
#         linear 0.2 u_angle 0
#     on idle:
#         linear 0.2 u_angle 3.14159*2/3

transform skin_opacity:
    on hover:
        linear 0.3 alpha 1.0
    on idle:
        linear 0.3 alpha 0.5

transform skin_grayscale:
    on hover:
        linear 0.3 matrixcolor SaturationMatrix(1)
    on idle:
        linear 0.3 matrixcolor SaturationMatrix(0)

transform gradient:
    shader "example.gradient_45"
    u_gradient_left (0.54, 0.36, 0.64, 1.0)
    u_gradient_right (0.0, 0.0, 0.0, 0.0)
    on hover:
        linear 0.2 u_gradient_right (0.54, 0.36, 0.64, 1.0)
        linear 0.2 u_gradient_left (0.0, 0.0, 0.0, 0.0)
    on idle:
        linear 0.2 u_gradient_left (0.54, 0.36, 0.64, 1.0)
        linear 0.2 u_gradient_right (0.0, 0.0, 0.0, 0.0)


transform gradient_idle:
    shader "example.gradient"
    u_gradient_left (1.0, 0.0, 0.0, 1.0)
    u_gradient_right (0.0, 0.0, 1.0, 1.0)

transform gradient_hover:
    shader "example.gradient"
    u_gradient_left (0.0, 0.0, 1.0, 1.0)
    u_gradient_right (1.0, 0.0, 0.0, 1.0)