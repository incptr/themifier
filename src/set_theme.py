import argparse
import yaml
import os
import subprocess


def insert_variables(command, config, theme):
    """
    Replace placeholders in a string with corresponding values from a dictionary.

    :param string: The input string containing placeholders.
    :param values: A dictionary mapping placeholder names to their values.
    :return: The string with placeholders replaced by their corresponding values.
    """
    for key, value in config["globals"].items():
        placeholder = "<{}>".format(key)
        command = command.replace(placeholder, str(value))
    for key, value in theme["theme"]["variables"].items():
        placeholder = "<{}>".format(key)
        command = command.replace(placeholder, str(value))
    for key, value in theme["theme"]["palette"].items():
        placeholder = "<{}>".format(key)
        command = command.replace(placeholder, str(value))
    return command


def run_update_command(command, config, theme):
    command = insert_variables(command, config, theme)
    print(f"Running {command}")
    subprocess.run(command.split(" "))
    return


def get_engine(engine):
    if engine == "perl":
        return ["perl", "-pi, -e"]
    elif engine == "sed":
        return ["sed", "-i"]
    raise ValueError("No valid regex engine provided.")


def do_change(change, engine, config, theme):
    regex = insert_variables(f"s/{change[0]}/{change[1]}/g", config, theme)
    target_file = insert_variables(change[2], config, theme)
    command = engine + [regex, target_file]
    print(f"Running {command}")
    subprocess.run(command)


def run_substititions(substitutions, config, theme):
    engine = get_engine(substitutions["engine"])
    for change in substitutions["changes"]:
        do_change(change, engine, config, theme)
    return


def parse_component(component, config, theme):
    if "cmd" in component.keys():
        run_update_command(component["cmd"], config, theme)
    if "substitutions" in component.keys():
        run_substititions(component["substitutions"], config, theme)


def update_components(config, theme):
    for component in config["components"]:
        if 'enabled' not in component.keys() or not component["enabled"]:
            continue
        parse_component(component, config, theme)


def get_theme(theme):
    theme_file = f"/home/s0001604/.config/themifier/themes/{theme}.yaml"
    if not os.path.isfile(theme_file):
        print(f"Theme not found in {theme_file}.")
        return -1
    with open(theme_file, 'r') as file:
        theme = yaml.safe_load(file)

    return theme


def get_config(config_file="/home/s0001604/.config/themifier/config.yaml"):
    if not os.path.isfile(config_file):
        print(f"config not found in {config_file}.")
        return -1
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    return config


def main():
    parser = argparse.ArgumentParser(
        prog='Themifier',
        description='Set a theme',
        epilog='Example use:\n python src/set_theme.py everforest')
    parser.add_argument('theme')           # positional argument

    args = parser.parse_args()
    theme = get_theme(args.theme)

    config = get_config()
    update_components(config, theme)


main()
