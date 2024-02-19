
import argparse
import yaml
import os
import subprocess


def read_update_policy_file(update_policy_file="/home/s0001604/.config/themifier/config.yaml"):
    if not os.path.isfile(update_policy_file):
        print(f"update_policy not found in {update_policy_file}.")
        return -1
    with open(update_policy_file, 'r') as file:
        update_policy = yaml.safe_load(file)

    return update_policy


class UpdatePolicy():
    def __init__(self):
        update_policy = read_update_policy_file()
        self.globals = self._extract_globals(update_policy)
        self.components = self._extract_components(update_policy)

    def _extract_globals(self, update_policy):
        return update_policy["globals"] if "globals" in update_policy.keys() else {}

    def _extract_components(self, update_policy):
        if "components" not in update_policy.keys():
            raise Exception("Update policy does not contain any components.")
        components = update_policy["components"]
        components_to_run = []

        for indx, component in enumerate(components):
            if "enabled" in component.keys() and component["enabled"]:
                components_to_run.append(component)
        return components_to_run
