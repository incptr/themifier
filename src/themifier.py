import argparse

from theme import Theme
from update_policy import UpdatePolicy
from component_updater import ComponentUpdater


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Themifier',
        description='Set a theme',
        epilog='Example use:\n python src/set_theme.py everforest')
    parser.add_argument('--theme', required=True)
    parser.add_argument('--verbose', required=False, action="store_true")

    args = parser.parse_args()

    theme = Theme(args.theme)
    update_policy = UpdatePolicy()

    component_updater = ComponentUpdater(theme, update_policy, args)
    component_updater.update()
