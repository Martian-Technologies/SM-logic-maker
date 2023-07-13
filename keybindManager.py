import json

class KeybindManager:
    keybinds = {}

    @staticmethod
    def loadKeybinds():
        with open('keybinds.json', 'r') as f:
            KeybindManager.keybinds = json.load(f)

    @staticmethod
    def setKeybind(key, action):
        if action not in KeybindManager.keybinds:
            raise Exception("Action not found: " + action)
        KeybindManager.keybinds[action] = key
        with open('keybinds.json', 'w') as f:
            json.dump(KeybindManager.keybinds, f, indent=4)

KeybindManager.loadKeybinds()
keybinds = KeybindManager.keybinds