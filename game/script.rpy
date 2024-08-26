init -1500 python:
    renpy.add_layer("clothes", "master")

    lily_clothes = ""

    def show_statement_replace(render_name, at_list=[], layer='master', what=None, zorder=0, tag=None, behind=[],atl=None):
        renpy.show(render_name, at_list=at_list, layer=layer, what=what, zorder=zorder, tag=tag, behind=behind,atl=atl)
        
        if lily_clothes is not "":
            print(render_name)
            print(lily_clothes)
            renpy.show(" ".join(render_name) + lily_clothes, at_list=at_list, layer="clothes", what=what, zorder=zorder, tag=tag, behind=behind,atl=atl)


define e = Character("Eileen")

define config.show = show_statement_replace


label start:
    menu:
        "Qual a cor da roupa de lily?"
        "Vermelho":
            $ lily_clothes = "_red"

        "Preto":
            $ lily_clothes = "_black"

        "Pink":
            $ lily_clothes = "_pink"


    show ep8 lilylewd_016

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"

    return
