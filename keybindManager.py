import json


class KeybindManager:
    """
    A class for managing keybindings for actions in a program.
    """

    keybinds = {}

    @staticmethod
    def loadKeybinds():
        """
        Loads the keybindings from a JSON file.
        """
        with open("keybinds.json", "r") as f:
            KeybindManager.keybinds = json.load(f)

    @staticmethod
    def setKeybind(key, action):
        """
        Sets a keybinding for a given action.

        :param key: The key to bind to the action.
        :param action: The action to bind the key to.
        """
        if action not in KeybindManager.keybinds:
            raise Exception("Action not found: " + action)
        KeybindManager.keybinds[action] = key
        with open("keybinds.json", "w") as f:
            json.dump(KeybindManager.keybinds, f, indent=4)


KeybindManager.loadKeybinds()
keybinds = KeybindManager.keybinds
