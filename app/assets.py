# -*- coding: utf-8 -*-
"""
    app.assets
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    asset "pipeline"
"""

from flask_assets import Environment, Bundle

# Other Assets.
app_css = Bundle(
    filters=("libsass", "cssmin"),
    output="cssmin/app.min.css"
)

app_js = Bundle(
    filters="jsmin",
    output="jsmin/app.min.js"
)


def init_app(app):
    web_assets = Environment(app)
    web_assets.register('app_css', app_css)
    web_assets.register('app_js', app_js)
    web_assets.manifest = 'cache' if not app.debug else False
    web_assets.cache = not app.debug
    web_assets.debug = app.debug
