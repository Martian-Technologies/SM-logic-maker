# def loop_func(events):
#     print("Loop function called.")
# def loop_intercept_function(app):
#     setattr(app.mainLoop, "loop", loop_func)


class Plugin:
    name = "Test Plugin 1"
    description = "This is a test plugin for testing the plugin manager."
    author = "Nikita"
    additions = {
        "startup": [
            # loop_intercept_function,
        ],
    }