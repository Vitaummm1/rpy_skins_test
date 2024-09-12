init -1 python:
    # Array de skins selecionadas
    skins_selected = []
    # Skins disponíveis. Utilizadas para troca de skins nos menus
    skins_available = {
        "julia": ["default", "2"],
        "susan": ["default", "1"],
        "simon": ["default", "1" ,"2"]
    }

    # Retorna as skins disponíveis para cada personagem. Utilizado para a troca de skins nos menus
    def get_character_skins(character):
        global skins_available
        return skins_available[character]

    # Método utilizado para encontrar qual skin está selecionada para o personagem. Caso não haja nenhuma, será retornada a skin default
    def get_selected_skin(character):
        global skins_selected
        for skin in skins_selected:
            if character in skin:
                return skin.replace("_", "")
        
        return (character + "default")

