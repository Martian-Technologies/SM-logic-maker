import os
import importlib
import pygame


class PluginManager:
    def __init__(self, app):
        block_menu = app.mainLoop.block_menu
        self.app = app
        LogicGridItem_base = importlib.import_module("logicGrid").LogicGridItem
        for plugin in os.listdir(os.path.join(os.path.dirname(__file__), "plugins")):
            if not plugin.endswith(".py"):
                continue
            # do something with plugin
            print(plugin)
            # import plugin and check if it has a Plugin class
            pluginModule = importlib.import_module("plugins." + plugin[:-3])
            if not hasattr(pluginModule, "Plugin"):
                print("Plugin " + plugin + " does not have a Plugin class.")
                continue
            pluginClass = getattr(pluginModule, "Plugin")
            # check if plugin has all required attributes
            if not hasattr(pluginClass, "name"):
                print("Plugin " + plugin + " does not have a name.")
                continue
            if not hasattr(pluginClass, "description"):
                print("Plugin " + plugin + " does not have a description.")
                continue
            if not hasattr(pluginClass, "author"):
                print("Plugin " + plugin + " does not have an author.")
                continue
            if not hasattr(pluginClass, "additions"):
                print("Plugin " + plugin + " does not have any additions.")
                continue
            # print addition types
            for additionType in pluginClass.additions:
                print(additionType)
                if additionType == "logicGridItems":
                    for item in pluginClass.additions[additionType]:
                        print(item)
                        self.addLogicGridItem(item, LogicGridItem_base, block_menu)
                elif additionType == "startup":
                    for func in pluginClass.additions[additionType]:
                        print(func)
                        func(self.app)
                else:
                    print("Unknown addition type: " + additionType)

    def addLogicGridItem(self, item, LogicGridItem_base, block_menu):
        print(item)
        # check if item has all required attributes
        if not hasattr(item, "name"):
            print("LogicGridItem does not have a name.")
            return
        if not hasattr(item, "icon_color"):
            print("LogicGridItem does not have an icon color.")
            return

        # make a copy of item that would be virtually "inherited" from LogicGridItem_base
        class LogicGridItem(LogicGridItem_base):
            name: str = item.name
            icon_color: pygame.color.Color = item.icon_color
            icon: pygame.surface.Surface = pygame.surface.Surface((100, 100))
            icon.fill(item.icon_color)

            def __init__(self, data=None) -> None:
                super().__init__(data, self.name, None)

        # add all the other attributes
        for attr in item.__dict__:
            if attr == "name" or attr == "icon_color":
                continue
            if attr.startswith("__"):
                continue
            print(attr)
            setattr(LogicGridItem, attr, getattr(item, attr))

        # add item to block menu
        block_menu.addItem(LogicGridItem)
