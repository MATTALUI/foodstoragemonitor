from flask import redirect, send_from_directory

class RootController:

    # @classmethod
    def root():
        return redirect("/storage-items")

    # @classmethod
    def static(path):
        return send_from_directory('static/assets', path)
