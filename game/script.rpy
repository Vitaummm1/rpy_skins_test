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
        for i in range(1, len(layers)):
            renpy.scene(layers[i])

    def show_statement_replace(render_name, at_list=[], layer='master', what=None, zorder=0, tag=None, behind=[], atl=None):
        global layers, stacked_master_layer, last_show_image, last_show_image_tuple
        # print(render_name, at_list, layer, what, zorder, tag, behind, atl)
        # Começa fazendo a limpeza das layers, apenas se não houver uma layer especificada
        if layer == "master":
            clear_layers()
        # Aqui obtém-se a configuração específica do arranjo das layers, do que deve ser exibido e onde
        layers_config = get_layers_config(" ".join(render_name))

        # Armazena a imagem que é mostrada e o tuple, para uso futuro pelo force_update_skins
        last_show_image = " ".join(render_name)
        last_show_image_tuple = render_name

        base_render_name = " ".join(render_name) # Nome do render. Ex.: ep8 lilysex_001
        check_render_layer = "{}_{}".format(base_render_name, layers[1]) # Nome para verificar se faz parte do sistema de layers. Ex.: ep8 lilysex_001_layer1
        
        # Verifica se a imagem possui sistema de camadas. Caso não possua, apenas faz o render normalmente
        if not renpy.has_image(check_render_layer):
            if zorder is None and base_render_name not in ["black", "config.gl_test_image"]:
                stacked_master_layer = []
                stacked_master_layer.append(last_show_image_tuple)
            elif base_render_name not in ["black", "config.gl_test_image"]:
                stacked_master_layer.append(last_show_image_tuple)
            # layers_last_show[layer] = last_show_image_tuple

            if "anim" in base_render_name and "skin" in base_render_name:
                check_render_skin = base_render_name.replace("_skin", "")
                render_skin = check_and_select_skin(check_render_skin)
                base_render_name = render_skin

            renpy.show(base_render_name, at_list=at_list, layer=layer, what=what, zorder=0, tag=tag, behind=behind, atl=atl)
            return

        # layers_last_show["master"] = ""

        # Iteração em cada camada para exibir uma imagem, caso haja
        for i in range(1, len(layers)):
            # Caso exista uma configuração de layer para este shot. Ex.: ["ep8 lilysex_001_layer1", "ep8 lilysex_001_layer3", "ep8 lilysex_001_layer2"]
            # Assim, ep8 lilysex_001_layer1 será exibido na layer1, ep8 lilysex_001_layer3 será exibido na layer2 e ep8 lilysex_001_layer2 será exibido na layer3
            # layers_last_show[layers[i]] = ""
            # renpy.scene(layers[i])
            if get_layers_config(base_render_name) is not None and len(layers_config) > i - 1: 
                render_layer = "{}_{}".format(base_render_name, layers_config[i - 1])
            else: # Caso não exista configuração de layer, os shots serão exibidos na configuração default de layers
                render_layer = "{}_{}".format(base_render_name, layers[i])
            
            # Faz a verificação se, para a layer que será exibida, há uma skin selecionada. Caso haja, o shot com a skin será exibido no lugar do default
            # Ex. de skin: ep8 lilysex_001_layer2_lily2 -> Se houver selecionada a skin _lily2 no array de skins_selected, essa imagem será exibida no lugar de ep8 lilysex_001_layer2
            render_layer = check_and_select_skin(render_layer)
            
            # Por fim, caso exista uma imagem para ser exibida, ela será exibida. Serve para evitar problemas em que há um "render_not_found"
            if renpy.has_image(render_layer):
                # layers_last_show[layers[i]] = last_show_image_tuple
                renpy.show(render_layer, at_list=at_list, layer=layers[i], what=what, zorder=zorder, tag=tag, behind=behind, atl=atl)

        stacked_master_layer = []


    def check_and_select_skin(render_layer):
        # Verifica se existe a imagem com skin, dentre as selecionadas, se não, exibe a default
        global skins_selected
        for skin in skins_selected:
            if "Default" not in skin:
                check_render_skin = "{}_{}".format(render_layer, skin)
                if renpy.has_image(check_render_skin):
                    return check_render_skin
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
        # show_statement_replace(last_show_image_tuple) # Faz atualização dos shots
        
        
    def update_skins_callback():
        # Este callback periódico executa a cada 20hz. Ele deverá ser executado, de fato, apenas se a variável to_update_context for True e não estiver no contexto de menu.
        # Caso esteja no menu e a variável to_update_context esteja True, nada ocorrerá, garantindo que a atualização das interações e do shot ocorra assim que voltar para o
        # jogo. Setar o to_update_context para True no final é imprescindível para garantir que este método não fique ocorrendo todas as vezes, o tempo todo
        global to_update_context, last_show_image_tuple, stacked_master_layer
        stacked_master_layer_helper = stacked_master_layer[:]
        if to_update_context and not _menu:
            if len(stacked_master_layer_helper):
                for item in stacked_master_layer_helper:
                    show_statement_replace(item)
            else:
                show_statement_replace(last_show_image_tuple)
            renpy.restart_interaction()
            to_update_context = False


define e = Character("Eileen")
define julia = Character(_("Julia"), color="#C161D4", voice_tag="julia")   
define susan = Character(_("Susan"), color="#8C91ED", voice_tag="susan") 
define simon = Character("Simon", color="#5995ED", voice_tag="simon")
define ep1_arcade_machine = Character(_("MACHINE"))
define d = dissolve
define config.periodic_callback = update_skins_callback # Callback para ser executado a cada 20hz
define config.show = show_statement_replace # Igual é no projeto principal do FreshWomen

# image susan1 = Movie(play="images/ep8 freetimejulia_001_2_layer1.webm", side_mask=True)

label start1:
    show ep8 susansex_001 with d
    simon "(I've waited a long time for this moment.)"
    simon "(And it's finally happening.)"
    show ep8 susansex_002 with d
    simon "(She called me a \"man\" twice.)"
    simon "(The time's come to show her she's right.)"
    show ep8 susansex_003 with d
    susan "We'll be more comfortable here in my room."
    susan "Well then..."
    show ep8 susansex_004 with d
    susan "..."
    simon "..."
    show ep8 susansex_005 with d
    simon "You're right."
    simon "Since we're here..."
    show ep8 susansex_006 with d
    simon "Let's get more comfortable."
    show ep8 susansex_007 with d
    susan "I thought you liked the uniform."
    simon "I did." (what_italic=True)
    show ep8 susansex_008 with d
    simon "You can keep it on if you'd like..." (what_italic=True)
    simon "For now." (what_italic=True)
    show ep8 susansex_008_1 with d
    simon "But since you're dressed like a waitress..."
    simon "Serve me."
    show ep8 susansex_009 with d
    susan "I don't think so."
    susan "Are you forgetting something?"
    show ep8 susansex_010 with d
    susan "I'm still your boss."
    simon "Oh, but I thought —" (what_italic=True)
    show ep8 susansex_011 with d
    susan "Stop talking."
    show ep8 susansex_011_1 with d
    pause 0.3
    show ep8 susansex_012 with d
    susan "And start working."
    simon "Yes, ma'am." (what_italic=True)
    show ep8 susansex_013 with d
    simon "You don't need to ask twice."

    show ep8 susansex_017 with d
    susan "I think it's about time we took off these clothes."
    show ep8 susansex_017_1 with d
    pause
    show ep8 susansex_017_2 with d
    pause
    show ep8 susansex_018 with d
    susan "So you can suck on everything else."
    simon "Yes, boss."
    show ep8 susansex_019 with d
    simon "It would be my pleasure."

    show ep8 susansex_023 with d
    simon "Your toys?"
    show ep8 susansex_023_1 with d
    simon "We can use some if you want."
    show ep8 susansex_023_2 with d
    susan "I would very much like that..." (what_italic=True)
    show ep8 susansex_024 with d
    susan "Can you go get them?"
    susan "They're in that drawer."
    show ep8 susansex_025 with d
    simon "Okay, I'll be right back."
    show ep8 susansex_026 with d
    simon "(What do we have here?)"
    show ep8 susansex_027 with d
    simon "(Okay... Which one should I use?)"

    show ep8 susansex_028 with d
    simon "I bet you'll like this one."
    susan "You'd win that bet..." (what_italic=True)
    susan "It's one of my favorites." (what_italic=True)

    show ep8 susansex_032 with d
    simon "What?"
    simon "Not yet..."
    show ep8 susansex_032_1 with d
    simon "We're just getting started."
    show ep8 susansex_033 with d
    simon "Let's set this aside for a bit." (what_italic=True)

    show ep8 susansex_034 with d
    simon "I hope you don't mind..."
    show ep8 susansex_035 with d
    pause 0.4
    show ep8 susansex_035_1 with d
    pause 0.4
    show ep8 susansex_035_2 with d
    simon "Being handcuffed for a while..."
    show ep8 susansex_036 with d
    simon "While I play with your body some more."

    show ep8 susansex_040 with d
    simon "Good to know..."
    show ep8 susansex_035 with d
    simon "But I don't want you to be tied up when you cum."
    simon "So let me give you a bit more freedom."

    show ep8 susansex_041 with d
    simon "Because I want to see you use these."
    susan "Hmm..." (what_italic=True)
    susan "Interesting choice." (what_italic=True)

    #Falas nova da Susan com a opção de Anal Beads

    show ep8 susansex_043_1 with d
    susan "I like them even better..."
    susan "In my tight little asshole..."

    show ep8 susansex_043_2 with d
    susan "Do you want to see?"

    menu:
        "I'd love to":
            show ep8 susansex_043_3 with d
            susan "Good."
            susan "I always like to start nice and easy..."
            susan "Spreading a bit of lube around, and feeling everything..."

            show ep8 susansex_043_4 with d
            susan "Oh my god!"
            susan "That felt amazing!"

            #Fim das falas novas da Susan de Anal Beads

            show ep8 susansex_044 with d
            simon "I enjoyed that."


        "No more toys.":
            show ep8 susansex_044 with d
            simon "I'd love to see that another time."


    show ep8 susansex_045 with d
    simon "But I think now it's time we moved on..." (what_italic=True)
    show ep8 susansex_046 with d
    simon "To this toy here."
    susan "Oh..." (what_italic=True)
    show ep8 susansex_047 with d
    susan "I've been eagerly awaiting this one."

    #Falas novas da Susan -> Blowjob teasing e throatfuck

    show ep8 susansex_047_2 with d
    susan "I can't wait to feel your whole dick in my mouth."

    show ep8 susansex_047_3 with d
    susan "I can see you want it too, Simon..."
    susan "You can tell me..."

    show ep8 susansex_047_4 with d
    susan "Whisper in my ear..."

    menu:
        "I want to fuck your throat hard":
            show ep8 susansex_047_4 with d
            simon "I want to fuck your throat."
            show ep8 susansex_047_5 with vpunch
            simon "Hard!"
            susan "Ahhh."

            show ep8 susansex_047_6 with d
            susan "You're a bad boy, huh?"

            show ep8 susansex_047_7 with d
            susan "I love it when you play rough with me."
            simon "Yeah?"
            simon "Then get down."

            show ep8 susansex_047_8 with d
            susan "Hmmm."
            susan "Like this?"
            simon "Yeah."
            simon "Now, open your mouth."

            show ep8 susansex_047_9 with d
            susan "You like being bossy, huh?"

            show ep8 susansex_047_10 with vpunch
            simon "You don't know the half of it."
            susan "Hmmmm."

            show ep8 susansex_047_11 with vpunch
            susan "What a nice surprise."

            show ep8 susansex_047_12 with d
            susan "Like this?"
            simon "Yeah."
            susan "And now you-"
            
            show ep8 susansex_047_13 with vpunch
            susan "Ahhhh."

            show ep8 susansex_047_14 with vpunch
            susan "That was amazing..."

            show ep8 susansex_047_15 with d
            susan "I want you inside me so bad!"
            simon "I know!"
            simon "I wanted you to get ready for my dick."

        "I want your pussy, now.":
            show ep8 susansex_047_4 with d
            simon "I want your pussy."
            simon "Now."

            show ep8 susansex_047_16 with d
            susan "Good boy."
            susan "You were teasing so good."
            simon "I wanted you to get ready for my dick."


    show ep8 susansex_047_1 with d
    susan "And now I'm ready for it."
    show ep8 susansex_048 with d
    simon "That's just what I wanted to hear."
    show ep8 susansex_048_1 with d
    simon "Because I couldn't wait any longer."

    show ep8 susansex_052 with d
    susan "Wait a moment..." (what_italic=True)
    show ep8 susansex_052_1 with d
    susan "I want to change positions." (what_italic=True)
    show ep8 susansex_053 with hpunch
    susan "You sit there..."

    show ep8 susansex_056 with d
    susan "(I'm just getting started.)"
    show ep8 susansex_057 with d
    susan "Lay down!"

    show ep8 susansex_058 with d
    susan "I want to ride you."

    show ep8 susansex_063 with d
    susan "Eyes up here, handsome."
    simon "Sorry, boss." (what_italic=True)
    show ep8 susansex_064 with d
    susan "Seems like you really like my breasts."
    simon "I do." (what_italic=True)
    show ep8 susansex_065 with d
    susan "Then I give you permission to play with them."

    show ep8 susansex_068 with d
    susan "And when I get really horny..."
    show ep8 susansex_069 with d
    susan "I like to end like this..."

    show ep8 susansex_073 with d
    susan "Aaaaaaaaahhhhhhh!!!!! Fuck!"
    show ep8 susansex_073_1 with d
    susan "..."
    show ep8 susansex_074 with d
    susan "That was incredible."
    susan "Now it's your turn to cum."
    show ep8 susansex_075 with d
    susan "And because you've exceeded my expectations..."
    susan "I'll let you choose."
    susan "Where do you want to cum?"

    menu:
        "Mouth":
            show ep8 susansex_075_1 with d
            pause
            show ep8 susansex_076 with d
            susan "In my mouth?"
            susan "Good choice."
            show ep8 susansex_077 with d
            simon "Aaaaaaaaahhhhhhh!!!!!"
            show ep8 susansex_078 with d
            susan "Mmm..."
            susan "Delicious."

        "Tits":
            show ep8 susansex_075_1 with d
            pause
            show ep8 susansex_079 with d
            susan "On my breasts?"
            susan "I figured you'd choose my girls."
            show ep8 susansex_080 with d
            simon "Aaaaaaaaahhhhhhh!!!!!"
            show ep8 susansex_081 with d
            susan "Mmmmm..."

        "Inside":
            show ep8 susansex_082_1 with d
            pause 0.2
            show ep8 susansex_082 with d
            susan "Inside of me?"
            susan "Sure..."
            show ep8 susansex_083 with d
            simon "Aaaaaaaaahhhhhhh!!!!!"
            show ep8 susansex_084 with d
            susan "Mmmmm..." (what_italic=True)
            susan "So hot..." (what_italic=True)

show ep8 susansex_085 with d
simon "Aaahh..."
simon "That was incredible."
show ep8 susansex_086 with d
simon "Susan..."
simon "You're amazing."
show ep8 susansex_087 with d
susan "Thank you, Simon."
susan "I enjoyed it too."
show ep8 susansex_088 with d
susan "Now, if you'll excuse me..."
simon "Where are you going?" (what_italic=True)
show ep8 susansex_089 with d
susan "To clean up. Then I should get some rest."
susan "If you'd like to take a shower, you can use the guest bathroom."
susan "Goodnight."
show ep8 susansex_090 with d
simon "Goodnight..."
show ep8 susansex_091 with d
simon "(Dude...)"
simon "(I can't believe it.)"
simon "(I just had sex with my boss!)"

return



label start:
#     # menu:
#     #     "Qual o modelo de roupa do Simon?"
#     #     "Padrão":
#     #         $ update_skins("simon", "Default")
#     #     "Roupa A":
#     #         $ update_skins("simon", "1")
#     #     "Roupa B":
#     #         $ update_skins("simon", "2")

#     # menu:
#     #     "Qual o modelo de roupa da Julia?"
#     #     "Padrão":
#     #         $ update_skins("julia", "Default")
#     #     "Roupa B":
#     #         $ update_skins("julia", "2")

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


show ep8 freetimejulia_003 with d
julia "I will end you all!"
julia "Aaaaahhhh!!!!!"
show ep8 freetimejulia_004 with vpunch
ep1_arcade_machine "GAME OVER!"
stop sound
show ep8 freetimejulia_005 with d
julia "Damn you!"
julia "This game's too hard!"
simon "Hey, Julia!" (what_italic=True)
call ep1_teste from _call_ep1_teste
show ep8 freetimejulia_006 with d
julia "Hey, Twinkle Toes!"

show bg
e 'limpar tela'

menu:
    "sem pelo":
        show susan_nova with dissolve
        e 'sem pelo'

    "leve pelo":
        show susan_nova
        show susan_nova_pubes_1 zorder 1000
        show ep8 anim_susannova_001_skin zorder 1000
        with dissolve
        e 'pubes 1'

    "muito pelo":
        show susan_nova
        show susan_nova_pubes_2 zorder 1000
        with dissolve
        e 'pubes 2'

show susan with dissolve
e 'limpa tela'

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
julia "3"
show ep8 freetimejulia_013 with d
simon "2"
simon "1"
show ep8 freetimejulia_099 with d
simon "Sem pelos :("
show ep8 freetimejulia_001_1 with d
simon "Com pelos! :)"
show ep8 freetimejulia_098 with d
simon "E se tiverem objetos na cena?"
show ep8 freetimejulia_001 with d
simon "Funciona mesmo assim! AW YEAH"
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
