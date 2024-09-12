init -1500 python:
    # Camadas que existirão no jogo
    layers = ["master", "layer1", "layer2", "layer3", "layer4", "layer5", "layer6"]
    layers_last_show = {
        "master": "",
        "layer1": "",
        "layer2": "",
        "layer3": "",
        "layer4": "",
        "layer5": "",
        "layer6": ""
    }
    stacked_master_layer = []

    # Arquivo de configuração de camadas para shots
    layers_config = {
        "ep8 freetimejulia_007": ["layer1", "layer3", "layer2"],
        "ep8 freetimejulia_003": ["layer1", "layer3", "layer2"]
    }

    
    def get_layers_config(shot): # Verifica no arquivo de configurações de layer se existe um array de configuração para o shot especificado
        global layers_config
        return layers_config.get(shot, None)