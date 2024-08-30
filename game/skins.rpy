init -1 python:
    skins_selected = []
    skins_available = {
        "julia": ["default", "2"],
        "simon": ["default", "1" ,"2"]
    }

    def get_character_skins(character):
        global skins_available
        return skins_available[character]

    def get_selected_skin(character):
        global skins_selected
        for skin in skins_selected:
            if character in skin:
                return skin.replace("_", "")
        
        return (character + "default")

