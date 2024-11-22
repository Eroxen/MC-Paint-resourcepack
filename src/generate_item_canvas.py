import json
from pathlib import Path

def pixel_model(xi, yi, grid_size=16, tintindex=0):
    step = 16 // grid_size

    x = xi * step
    y = 16 - (yi * step)

    return {
    "parent": "mcpaint:item/pixel_canvas/parent",
    "elements": [
        {   "from": [ x, y - step, 7.49 ],
            "to": [ x + step, y, 8.51 ],
            "faces": {
                "north": { "uv": [ x + step, 16 - (y - step), x, 16 - y ], "texture": "#0", "tintindex": tintindex },
                "south": { "uv": [ x, 16 - (y - step), x + step, 16 - y ], "texture": "#0", "tintindex": tintindex },
            }
        }
    ]
}

def pixel_composite(min_xi, max_xi, min_yi, max_yi, cmd_flags_start=0, cmd_tints_start=0):
    models = []
    for xi in range(min_xi, max_xi):
        for yi in range(min_yi, max_yi):
            pixel_index = (yi - min_yi) * (max_xi - min_xi) + xi - min_xi
            models.append(
                {
                    "type": "minecraft:condition",
                    "property": "minecraft:custom_model_data",
                    "index": pixel_index + cmd_flags_start,
                    "on_true": {
                        "type": "minecraft:model",
                        "model": f"mcpaint:item/pixel_canvas/{xi}_{yi}",
                        "tints": [
                            {
                                "type": "minecraft:custom_model_data",
                                "index": pixel_index + cmd_tints_start,
                                "default": -1
                            }
                        ]
                    },
                    "on_false": {
                        "type": "minecraft:empty"
                    }
                }
            )
    return models

def variant_switch(shape):
    return {
        "type": "minecraft:select",
        "property": "minecraft:custom_model_data",
        "index": 0,
        "cases": [
            {
                "when": variant,
                "model": {
                    "type": "minecraft:model",
                    "model": f"mcpaint:item/custom_painting/{variant}_{shape}"
                }
            } for variant in ["empty", "blackboard", "puter"]
        ],
        "fallback": {
            "type": "minecraft:model",
            "model": f"mcpaint:item/custom_painting/canvas_{shape}"
        }
    }

def main():
    # generate pixel models
    pth = Path("..")/"assets"/"mcpaint"/"models"/"item"/"pixel_canvas"/"parent.json"
    pth.parents[0].mkdir(parents=True,exist_ok=True)
    with open(pth, 'w') as file:
        json.dump({
            "textures": {
                "0": "mcpaint:item/pixel_canvas"
            },
            "gui_light": "front",
            "display": {
                "ground": {
                    "rotation": [ 0, 0, 0 ],
                    "translation": [ 0, 2, 0],
                    "scale":[ 0.5, 0.5, 0.5 ]
                },
                "head": {
                    "rotation": [ 0, 180, 0 ],
                    "translation": [ 0, 13, 7],
                    "scale":[ 1, 1, 1]
                },
                "thirdperson_righthand": {
                    "rotation": [ 0, 0, 0 ],
                    "translation": [ 0, 3, 1 ],
                    "scale": [ 0.55, 0.55, 0.55 ]
                },
                "firstperson_righthand": {
                    "rotation": [ 0, -90, 25 ],
                    "translation": [ 1.13, 3.2, 1.13],
                    "scale": [ 0.68, 0.68, 0.68 ]
                },
                "fixed": {
                    "rotation": [ 0, 180, 0 ],
                    "scale": [ 1, 1, 1 ]
                }
            }
        }, file, indent=2)
    
    for xi in range(2,14):
        for yi in range(3,15):
            pth = Path("..")/"assets"/"mcpaint"/"models"/"item"/"pixel_canvas"/f"{xi}_{yi}.json"
            with open(pth, 'w') as file:
                json.dump(pixel_model(xi, yi), file)
    
    for variant in ["canvas", "blackboard", "puter", "empty"]:
        for shape in ["small", "tall", "wide", "big"]:
            pth = Path("..")/"assets"/"mcpaint"/"models"/"item"/"custom_painting"/f"{variant}_{shape}.json"
            pth.parents[0].mkdir(parents=True,exist_ok=True)
            with open(pth, 'w') as file:
                json.dump({
                    "parent": "item/generated", 
                    "textures": {
                        "layer0": f"mcpaint:item/custom_painting/{variant}_{shape}"
                    }
                }, file, indent=2)
    
    pth = Path("..")/"assets"/"mcpaint"/"items"/"custom_painting.json"
    pth.parents[0].mkdir(parents=True,exist_ok=True)
    with open(pth, 'w') as file:
        json.dump({
            "model": {
                "type": "minecraft:range_dispatch",
                "property": "minecraft:custom_model_data",
                "scale": 1.0,
                "index": 0,
                "entries": [
                    {
                        "threshold": 2.0,
                        "model": {
                            "type": "minecraft:range_dispatch",
                            "property": "minecraft:custom_model_data",
                            "scale": 1.0,
                            "index": 1,
                            "entries": [
                                {
                                    "threshold": 2.0,
                                    "model": {
                                        "type": "composite",
                                        "models": [
                                            variant_switch("big")
                                        ] + pixel_composite(2, 14, 3, 15)
                                    }
                                }
                            ],
                            "fallback": {
                                "type": "composite",
                                "models": [
                                    variant_switch("wide")
                                ] + pixel_composite(2, 14, 5, 13)
                            }
                        }
                    }
                ],
                "fallback": {
                    "type": "minecraft:range_dispatch",
                    "property": "minecraft:custom_model_data",
                    "scale": 1.0,
                    "index": 1,
                    "entries": [
                        {
                            "threshold": 2.0,
                            "model": {
                                "type": "composite",
                                "models": [
                                    variant_switch("tall")
                                ] + pixel_composite(4, 12, 3, 15)
                            }
                        }
                    ],
                    "fallback": {
                        "type": "composite",
                        "models": [
                            variant_switch("small")
                        ] + pixel_composite(4, 12, 5, 13)
                    }
                }
            }
        }, file, indent=2)



if __name__ == '__main__':
    main()