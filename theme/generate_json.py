import json

# Generates json to be read into pygame_ui.
# reads in prototypes, replacing relevant info.
# custom hierarchies per prototype.

prototype_file: str = "theme/proto.json"
output_file: str = "theme/buttons_generated.json"

button_ids = {
    "#thopter_button": "0,0,46,38",
    "#tardigrade_button": "138,0,46,38",
    "#sawmill_button": "230,0,46,38",
}

with open(prototype_file, "r") as input:
    prototypes = json.load(input)
    button_proto = prototypes["#button_proto"]

    export = {}
    # set placeholder button
    export["button"] = button_proto

    for id in button_ids:
        export[id] = json.loads(json.dumps(button_proto))
        export[id]["images"]["normal_images"][1]["sub_surface_rect"] = button_ids[id]
        export[id]["images"]["selected_images"][1]["sub_surface_rect"] = button_ids[id]

    with open(output_file, "w") as output:
        json.dump(export, output, indent=2)
