class imported_test_item_1:
    name = "test item 1"
    icon_color = (255, 0, 0)



class Plugin:
    name = "Test Plugin 1"
    description = "This is a test plugin for testing the plugin manager."
    author = "Nikita"
    additions = {
        "logicGridItems": [
            imported_test_item_1,
        ],
        # could add more in the future
    }