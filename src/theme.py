import argparse
import yaml
import os
import subprocess

MINIMUM_PALETTE = ["color0",
                   "color1",
                   "color2",
                   "color3",
                   "color4",
                   "color5",
                   "color6",
                   "color7"]

def read_theme_config_file(theme_name):
    theme_file = f"/home/s0001604/.config/themifier/themes/{theme_name}.yaml"
    if not os.path.isfile(theme_file):
        print(f"Theme not found in {theme_file}.")
        return -1
    with open(theme_file, 'r') as file:
        theme = yaml.safe_load(file)
    return theme

class Theme():
    def __init__(self, theme_name):
        theme_config = read_theme_config_file(theme_name)
        self.variables = _extract_variables(theme_config)
        self.palette = _extract_palette(theme_config)

    def _extract_variables(self, theme_config):
        return theme_config["variables"] if "variables" in theme_config.keys() else {}

    def _extract_palette(self, theme_config):
        if "palette" not in theme_config.keys():
            raise Exception("Theme does not contain a palette.")
        palette = theme_config["palette"]
        _verify_palette(palette)

    def _verify_palette(self, palette):
        for color in MINIMUM_PALETTE:
            if color not in palette:
                raise Exception(f"Palette does not contain minimum configuration:\n{MINIMUM_PALETTE}")
