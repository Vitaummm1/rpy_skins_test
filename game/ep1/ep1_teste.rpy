label ep1_teste:

    scene black with dissolve

    call screen skins_menu([{"character": "julia", "image":"default", "text": "Roupa de banho"}, {"character": "julia", "image": "2", "text": "Roupa padrão"}], "Que roupa Julia deveria vestir?")

    # menu:
    #     "Simon 1":
    #         $update_skins("simon", "1")
    #     "Simon 2":
    #         $update_skins("simon", "2")
    #     "Julia 1":
    #         $update_skins("julia", "1")
    #     "Julia 2":
    #         $update_skins("julia", "2")
return