import subprocess
import re


class ComponentUpdater():
    def __init__(self, theme, config, args):
        self.theme = theme
        self.up = config
        self.args = args

    def _run_command(self, command):
        if not self.args.verbose:
            return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Running {command}")
        return subprocess.run(command)

    def _insert_variables(self, command):
        """
        Replace placeholders in a string with corresponding values from a dictionary.

        :param string: The input string containing placeholders.
        :param values: A dictionary mapping placeholder names to their values.
        :return: The string with placeholders replaced by their corresponding values.
        """
        for key, value in self.up.globals.items():
            placeholder = "<{}>".format(key)
            command = command.replace(placeholder, str(value))
        for key, value in self.theme.variables.items():
            placeholder = "<{}>".format(key)
            command = command.replace(placeholder, str(value))
        for key, value in self.theme.palette.items():
            placeholder = "<{}>".format(key)
            command = command.replace(placeholder, str(value))
        # Check for remaining variable syntax and raise exception
        unresolved_variable = re.findall("<\w+>", command)
        if unresolved_variable:
            print(
                f"Variable(s) {unresolved_variable} were not "
                "found in theme variables or update policy globals.")
            return False, command

        return True, command

    def _run_update_command(self, command):
        success, command = self._insert_variables(command)
        if not success:
            return

        self._run_command(command.split(" "))
        return

    def _get_engine(self, engine):
        if engine == "perl":
            return ["perl", "-pi, -e"]
        elif engine == "sed":
            return ["sed", "-i"]
        raise ValueError("No valid regex engine provided.")

    def _do_change(self, change, engine):
        success, regex = self._insert_variables(f"s/{change[0]}/{change[1]}/g")
        if not success:
            return

        success, target_file = self._insert_variables(change[2])
        if not success:
            return

        command = engine + [regex, target_file]
        self._run_command(command)

    def _run_substititions(self, substitutions):
        engine = self._get_engine(substitutions["engine"])
        for change in substitutions["changes"]:
            self._do_change(change, engine)
        return

    def _parse_component(self, component):
        if "cmd" in component.keys():
            self._run_update_command(component["cmd"])
        if "substitutions" in component.keys():
            self._run_substititions(component["substitutions"])

    def update(self):
        for component in self.up.components:
            self._parse_component(component)
