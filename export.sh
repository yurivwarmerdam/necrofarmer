aseprite -b --layer=sprite --layer="Layer 1" --layer="Layer 2" --split-slices art/src/buildings.aseprite  --color-mode rgb --save-as art/{slice}.png;
aseprite -b --split-slices art/src/ui_spritesheet.aseprite --color-mode rgb --save-as art/{slice}.png;
