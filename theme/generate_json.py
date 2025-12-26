import json
from pprint import pprint


button_ids = {
    "#thopter_button": "0,0,46,38",
    "#tardigrade_button": "138,0,46,38",
}

with open("theme/proto.json", "r") as input:
    prototypes = json.load(input)
    button_proto = prototypes["#button_proto"]

    export = {}
    # set placeholder button
    export["button"] = button_proto

    for id in button_ids:
        export[id] = json.loads(json.dumps(button_proto))
        export[id]["images"]["normal_images"][1]["sub_surface_rect"] = button_ids[id]
        export[id]["images"]["selected_images"][1]["sub_surface_rect"] = button_ids[id]

    with open("theme/buttons.json", "w") as output:
        json.dump(export, output, indent=2)
