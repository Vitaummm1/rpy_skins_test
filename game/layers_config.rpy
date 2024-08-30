init -1500 python:
    layers = ["master", "layer1", "layer2", "layer3", "layer4", "layer5", "layer6"]
    layers_config = {
        "ep8 freetimejulia_007": ["layer1", "layer3", "layer2"],
        "ep8 freetimejulia_003": ["layer1", "layer3", "layer2"]
    }

    def get_layers_config(shot):
        global layers_config
        return layers_config.get(shot, None)