init -1000 python:
    skins_selected = []
    last_show_image = ""
    last_show_image_tuple = {}
    to_update_context = False


    def create_layers(): # Este método é responsável por inicializar as layers
        global layers
        for i in range(1, len(layers)):
            renpy.add_layer(layers[i], layers[i-1])

    create_layers()

    def clear_layers(): # Este método faz a limpeza das layers, iterando sobre cada uma delas e limpando a exibição
        global layers
        for layer in layers:
            renpy.scene(layer)

    def show_statement_replace(render_name, at_list=[], layer='master', what=None, zorder=0, tag=None, behind=[], atl=None):
        global layers, last_show_image, last_show_image_tuple
        # Começa fazendo a limpeza das layers
        clear_layers()
        # Aqui obtém-se a configuração específica do arranjo das layers, do que deve ser exibido e onde
        layers_config = get_layers_config(" ".join(render_name))

        # Armazena a imagem que é mostrada e o tuple, para uso futuro pelo force_update_skins
        last_show_image = " ".join(render_name[:2])
        last_show_image_tuple = render_name

        base_render_name = " ".join(render_name) # Nome do render. Ex.: ep8 lilysex_001
        check_render_layer = "{}_{}".format(base_render_name, layers[1]) # Nome para verificar se faz parte do sistema de layers. Ex.: ep8 lilysex_001_layer1
        
        # Verifica se a imagem possui sistema de camadas. Caso não possua, apenas faz o render normalmente
        if not renpy.has_image(check_render_layer):
            renpy.show(base_render_name, at_list=at_list, layer=layer, what=what, zorder=zorder, tag=tag, behind=behind, atl=atl)
            return

        # Iteração em cada camada para exibir uma imagem, caso haja
        for i in range(1, len(layers)):
            # Caso exista uma configuração de layer para este shot. Ex.: ["ep8 lilysex_001_layer1", "ep8 lilysex_001_layer3", "ep8 lilysex_001_layer2"]
            # Assim, ep8 lilysex_001_layer1 será exibido na layer1, ep8 lilysex_001_layer3 será exibido na layer2 e ep8 lilysex_001_layer2 será exibido na layer3
            if layers_config is not None and len(layers_config) > i - 1: 
                render_layer = "{}_{}".format(base_render_name, layers_config[i - 1])
            else: # Caso não exista configuração de layer, os shots serão exibidos na configuração default de layers
                render_layer = "{}_{}".format(base_render_name, layers[i])
            
            # Faz a verificação se, para a layer que será exibida, há uma skin selecionada. Caso haja, o shot com a skin será exibido no lugar do default
            # Ex. de skin: ep8 lilysex_001_layer2_lily2 -> Se houver selecionada a skin _lily2 no array de skins_selected, essa imagem será exibida no lugar de ep8 lilysex_001_layer2
            render_layer = check_and_select_skin(render_layer)
            
            # Por fim, caso exista uma imagem para ser exibida, ela será exibida. Serve para evitar problemas em que há um "render_not_found"
            if renpy.has_image(render_layer):
                renpy.show(render_layer, at_list=at_list, layer=layers[i], what=what, zorder=zorder, tag=tag, behind=behind, atl=atl)


    def check_and_select_skin(render_layer):
        # Verifica se existe a imagem com skin, dentre as selecionadas, se não, exibe a default
        global skins_selected
        for skin in skins_selected:
            if "Default" not in skin:
                check_render_layer = "{}_{}".format(render_layer, skin)
                if renpy.has_image(check_render_layer):
                    return check_render_layer
        return render_layer

    def update_skins(character, look):
        # Este método é utilizado para mudar as skins num contexto de menu. Ou seja, se há escolhas e o próximo shot deverá mostrar a skin atualizada, use este método
        global skins_selected
        new_skin = character + look

        # Verifica se já existe uma entrada para o personagem e atualiza ou insere nova
        for i, item in enumerate(skins_selected):
            if character in item:
                skins_selected[i] = new_skin
                break
        else:
            skins_selected.append(new_skin)


    def force_update_skins(character, look):
        # Este método é utilizado para mudar as skins enquanto o jogo está acontecendo. Ou seja, se a mudança de skin precisar ser instantânea, enquanto o jogo acontece, use este método
        global last_show_image_tuple, to_update_context
        update_skins(character, look) # Faz a atualização do array de skins_selected
        to_update_context = True # Marca como positivo para o update_skins_callback ser executado
        show_statement_replace(last_show_image_tuple) # Faz atualização dos shots
        
        
    def update_skins_callback():
        # Este callback periódico executa a cada 20hz. Ele deverá ser executado, de fato, apenas se a variável to_update_context for True e não estiver no contexto de menu.
        # Caso esteja no menu e a variável to_update_context esteja True, nada ocorrerá, garantindo que a atualização das interações e do shot ocorra assim que voltar para o
        # jogo. Setar o to_update_context para True no final é imprescindível para garantir que este método não fique ocorrendo todas as vezes, o tempo todo
        global to_update_context, last_show_image_tuple
        if to_update_context and not _menu:
            show_statement_replace(last_show_image_tuple)
            renpy.restart_interaction()
            to_update_context = False


define e = Character("Eileen")
define julia = Character(_("Julia"), color="#C161D4", voice_tag="julia")
define simon = Character("Simon", color="#5995ED", voice_tag="simon")
define ep1_arcade_machine = Character(_("MACHINE"))
define d = dissolve
define config.periodic_callback = update_skins_callback # Callback para ser executado a cada 20hz
define config.show = show_statement_replace # Igual é no projeto principal do FreshWomen

# image susan1 = Movie(play="images/ep8 freetimejulia_001_2_layer1.webm", side_mask=True)

label start:
    # menu:
    #     "Qual o modelo de roupa do Simon?"
    #     "Padrão":
    #         $ update_skins("simon", "Default")
    #     "Roupa A":
    #         $ update_skins("simon", "1")
    #     "Roupa B":
    #         $ update_skins("simon", "2")

    # menu:
    #     "Qual o modelo de roupa da Julia?"
    #     "Padrão":
    #         $ update_skins("julia", "Default")
    #     "Roupa B":
    #         $ update_skins("julia", "2")

    # show ep8 lilylewd_005
    # e "You've created a new Ren'Py game."
    # e "Once you add a story, pictures, and music, you can release it to the world!"

    # show ep8 lilylewd_010
    # e "You've created a new Ren'Py game."
    # e "Once you add a story, pictures, and music, you can release it to the world!"

    # show ep8 lilylewd_012
    # e "You've created a new Ren'Py game."
    # e "Once you add a story, pictures, and music, you can release it to the world!"

    # show ep8 freetimejulia_001
    # e "You've created a new Ren'Py game."
    # e "Once you add a story, pictures, and music, you can release it to the world!"


    show ep8 freetimejulia_001 with d
    simon "teste de pelos pubianos"
    show ep8 freetimejulia_001_1 with d
    simon "teste de pelos pubianos"
    show ep8 freetimejulia_001_2
    show dragon_move with d
    simon "teste de pelos pubianos"
    # show ep8 freetimejulia_001_4 with d
    # simon "Dragon Move freetime"

    show ep8 freetimejulia_003 with d
    julia "I will end you all!"
    julia "Aaaaahhhh!!!!!"
    show ep8 freetimejulia_004 with vpunch
    ep1_arcade_machine "GAME OVER!"
    stop sound
    show ep8 freetimejulia_005 with d
    call ep1_teste
    julia "Damn you!"
    julia "This game's too hard!"
    simon "Hey, Julia!" (what_italic=True)
    show ep8 freetimejulia_006 with d
    julia "Hey, Twinkle Toes!"
    show ep8 freetimejulia_007 with d
    julia "Glad you came!"

    show ep8 freetimejulia_008 with d
    julia "..."
    show ep8 freetimejulia_009 with d
    simon "..."

    show ep8 freetimejulia_010 with d
    simon "How are you?"
    show ep8 freetimejulia_011 with d
    julia "I'm just happy enough to get out of my house for a bit."
    julia "I didn't even see you come in."
    show ep8 freetimejulia_012 with d
    julia "I was distracted by an alien massacre."
    julia "How are you?"
    show ep8 freetimejulia_013 with d
    simon "Just happy to see you too."
    simon "Especially after the last time we met."
    show ep8 freetimejulia_014 with d
    julia "Oh... Sorry about that."
    julia "I don't know what came over me."
    show ep8 freetimejulia_013 with d
    simon "No need to apologize."
    show ep8 freetimejulia_015 with d
    simon "I certainly had a good time."
    simon "I hope we can have our next adventure somewhere more private next time."
    show ep8 freetimejulia_014 with d
    julia "Me too."
    julia "Well then..."
    show ep8 freetimejulia_016 with d
    julia "What were those documents anyway?"
    julia "What did you and that girl do to make Donna so mad?"
    show ep8 freetimejulia_013 with d
    simon "Nothing..."
    simon "She just wanted to know about our address. That's all."
    show ep8 freetimejulia_016 with d
    julia "Hmm..."
    julia "She's sort of nuts."
    show ep8 freetimejulia_017 with d
    julia "Ah, right."
    show ep8 freetimejulia_018 with d
    julia "I wanted to show you something. Come here!"
    show ep8 freetimejulia_019 with d
    julia "You see?"
    simon "Yeah... BPV will be performing in Las Vegas in a few days."
    show ep8 freetimejulia_020 with d
    julia "Exactly! It's so awesome!"
    show ep8 freetimejulia_021 with d
    julia "You know about them, right?"

    menu:
        "Of course I know them.":
            show ep8 freetimejulia_022 with d
            simon "Do I know them?"
            show ep8 freetimejulia_023 with d
            simon "They're the Bulletproof Vigilantes!"
            simon "They're only the best K-pop group of our generation."
            show ep8 freetimejulia_020 with d
            julia "I agree!"
            julia "They're geniuses!"
            show ep8 freetimejulia_022_2 with hpunch
            simon "I learned the choreography to all their songs."

        "I think I've heard of them.":
            show ep8 freetimejulia_024 with d
            simon "They're a K-pop group, right?"
            simon "I think I saw a song of theirs on Dance Dance Supreme."
            show ep8 freetimejulia_022_2 with hpunch
            simon "I do like the choreography on that one."
            show ep8 freetimejulia_021 with d
            julia "You're kidding, right?"
            show ep8 freetimejulia_025 with d
            julia "They're not \"a\" group. They're \"the\" group!"

        "Isn't BPV a disease?":
            show ep8 freetimejulia_024 with d
            simon "BPV..."
            show ep8 freetimejulia_026 with d
            simon "Isn't that a disease?"
            simon "Something about vertigo?"
            simon "My uncle died from that."
            simon "Sort of a weird name for a music group."
            show ep8 freetimejulia_021 with d
            julia "You seriously don't know them?"
            julia "They're even featured on Dance Dance Supreme!"
            show ep8 freetimejulia_025 with d
            julia "You have to know them!"
            show ep8 freetimejulia_027 with d
            julia "You disappoint me..."
            julia "I don't think we can be friends right now."
            show ep8 freetimejulia_026 with d
            simon "Are you for real?"
            simon "I'll look them up then. I promise."
            show ep8 freetimejulia_025 with d
            julia "You'd better, Twinkle Toes."
            show ep8 freetimejulia_028 with d
            julia "I'm only giving you a few days to memorize all their songs."

    show ep8 freetimejulia_028 with d
    julia "We have to get to that show!"
    show ep8 freetimejulia_029 with d
    julia "I'd do anything..."
    julia "I mean really, anything to see them up close."
    show ep8 freetimejulia_024 with d
    simon "Is this an invitation?"
    julia "An invitation? It's a summons!"
    show ep8 freetimejulia_028_3 with d
    julia "You are required by law to go with me."
    show ep8 freetimejulia_030 with d
    simon "All right..."
    simon "But what about your mom?"
    show ep8 freetimejulia_031 with d
    julia "Oh, she definitely won't be tagging along."
    show ep8 freetimejulia_030 with d
    simon "Hahaha."
    simon "You know what I mean."
    show ep8 freetimejulia_032 with d
    julia "I'll find some way to convince her."
    show ep8 freetimejulia_032_1 with d
    julia "So, what do you say?"
    show ep8 freetimejulia_032_2 with d
    simon "We can go together!"
    show ep8 freetimejulia_028_1 with d
    julia "Sounds like a plan."
    show ep8 freetimejulia_033 with d
    simon "(Huh?)"
    simon "(A text from Chloe!)"
    show ep8 freetimejulia_034 with d
    simon "(Oh, shit! Right!)"
    simon "(I promised I'd join her book club!)"
    simon "(But this time, I don't even have a good excuse for her.)"
    simon "(I hope Chloe doesn't get too upset.)"
    show ep8 freetimejulia_035 with d
    simon "Sorry, Julia, I really have to go."
    simon "I promised someone I'd be somewhere, and it totally slipped my mind."
    simon "I'm so sorry."
    simon "I promise I'll make it up to you later."
    show ep8 freetimejulia_036 with d
    julia "I'll hold you to that, Twinkle Toes."
    julia "And next time, we should arrange to meet in a more private location."
    julia "So we can continue our adventure at Donna's office."
    show ep8 freetimejulia_037 with d
    simon "I'm totally with you."
    simon "In the meantime..."
    show ep8 freetimejulia_038 with d
    simon "(We'll keep doing what we can.)"
    show ep8 freetimejulia_039 with d
    julia "Since you have to go, I'll stop by my work and spend a few hours there..."
    julia "I told my mom I would do it."
    julia "And it's quite possible that she will call there to confirm."
    show ep8 freetimejulia_040 with d
    simon "You know, Julia..."
    simon "You should have a talk with your mother."
    show ep8 freetimejulia_041 with d
    julia "To talk? With my mother?"
    julia "What do you mean?"
    show ep8 freetimejulia_042 with d
    simon "She needs to understand that you're an adult and that you can make your own decisions now."
    simon "She's only going to realize that if you bring it up with her."
    show ep8 freetimejulia_043 with d
    julia "I don't know..."
    julia "We're talking about my mother."
    show ep8 freetimejulia_044 with d
    julia "She's crazy."
    show ep8 freetimejulia_045 with d
    simon "Trust me."
    simon "You should give it a try."
    show ep8 freetimejulia_045_1 with d
    julia "Ok... I promise I'll think about it."
    show ep8 freetimejulia_046 with d
    julia "Goodbye!"

    return
