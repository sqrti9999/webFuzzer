from flask import Flask, render_template
from . import crawl


class WebInterface:
    def __init__(self):
        # Set variables

        # Configure app
        self.app = Flask(__name__)
        self.make_route()

    def make_route(self):
        @self.app.route('/')
        def index():
            return render_template('main.html', title='webFuzzer')

        self.app.register_blueprint(crawl.bp)
        return
