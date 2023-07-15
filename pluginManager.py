import os
import importlib
import pygame


class PluginManager:
    """
    A class that manages the loading and initialization of plugins for the SM Logic Maker application.

    Attributes:
        app (SMLogicMaker): The main application instance.
    """

    def __init__(self, app):
        """
        Initializes a new instance of the PluginManager class.

        Args:
            app (SMLogicMaker): The main application instance.
        """
        block_menu = app.mainLoop.block_menu
        self.app = app
        LogicGridItem_base = importlib.import_module("logicGrid").LogicGridItem

        # Iterate over all files in the "plugins" directory and load each plugin
        for plugin in os.listdir(os.path.join(os.path.dirname(__file__), "plugins")):
            if not plugin.endswith(".py"):
                continue
            # do something with plugin
            print(plugin)

            # Import the plugin module and check if it has a Plugin class
            pluginModule = importlib.import_module("plugins." + plugin[:-3])
            if not hasattr(pluginModule, "Plugin"):
                print("Plugin " + plugin + " does not have a Plugin class.")
                continue
            pluginClass = getattr(pluginModule, "Plugin")

            # Check if the plugin has all required attributes
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

            # Iterate over the plugin's additions and add them to the application
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
        """
        Adds a LogicGridItem to the application's block menu.

        Args:
            item (LogicGridItem): The LogicGridItem to add.
            LogicGridItem_base (type): The base class for LogicGridItems.
            block_menu (BlockMenu): The application's block menu.
        """
        print(item)

        # Check if the item has all required attributes
        if not hasattr(item, "name"):
            print("LogicGridItem does not have a name.")
            return
        if not hasattr(item, "icon_color"):
            print("LogicGridItem does not have an icon color.")
            return

        # Create a new class that "inherits" from LogicGridItem_base and add the item's attributes to it
        class LogicGridItem(LogicGridItem_base):
            name: str = item.name
            icon_color: pygame.color.Color = item.icon_color
            icon: pygame.surface.Surface = pygame.surface.Surface((100, 100))
            icon.fill(item.icon_color)

            def __init__(self, data=None) -> None:
                super().__init__(data, self.name, None)

        for attr in item.__dict__:
            if attr == "name" or attr == "icon_color":
                continue
            if attr.startswith("__"):
                continue
            print(attr)
            setattr(LogicGridItem, attr, getattr(item, attr))

        # Add the new LogicGridItem to the block menu
        block_menu.addItem(LogicGridItem)
