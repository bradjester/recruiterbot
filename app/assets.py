# -*- coding: utf-8 -*-
"""
    app.assets
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    asset "pipeline"
"""

from flask_assets import Environment, Bundle

# Other Assets.
app_css = Bundle(
    "scss/base.scss",
    filters=("libsass", "cssmin"),
    output="cssmin/app.min.css"
)

app_js = Bundle(
    "vendor/jquery-2.1.4.js",
    "vendor/lodash.js",
    "vendor/foundation/foundation.min.js",
    "vendor/foundation-datepicker/foundation-datepicker.js",
    "vendor/datatables-1.10.10/dataTables.js",
    "vendor/datatables-1.10.10/dataTables.foundation.js",
    "vendor/datatables-1.10.10/dataTables.buttons.js",
    "vendor/datatables-1.10.10/dataTables.buttons.html5.js",
    "vendor/dropzone-4.2.0/dropzone.js",
    'vendor/autosize-3.0.14.js',
    'vendor/notify/notify.js',
    'vendor/string-format.js',
    'vendor/clipboard.min.js',
    filters="jsmin",
    output="jsmin/app.min.js"
)

# Admin Assets.
admin_css = Bundle(
    "scss/admin.scss",
    filters=("libsass", "cssmin"),
    output="cssmin/admin.min.css"
)

admin_js = Bundle(
    "vendor/jquery-2.1.4.js",
    "vendor/lodash.js",
    "vendor/foundation/foundation.min.js",
    "vendor/foundation-datepicker/foundation-datepicker.js",
    "vendor/datatables-1.10.10/dataTables.js",
    "vendor/datatables-1.10.10/dataTables.foundation.js",
    "vendor/datatables-1.10.10/dataTables.buttons.js",
    "vendor/datatables-1.10.10/dataTables.buttons.html5.js",
    "vendor/dropzone-4.2.0/dropzone.js",
    'vendor/autosize-3.0.14.js',
    'vendor/notify/notify.js',
    'vendor/string-format.js',
    'vendor/clipboard.min.js',
    filters="jsmin",
    output="jsmin/admin.min.js"
)


def init_app(app):
    web_assets = Environment(app)
    web_assets.register('app_css', app_css)
    web_assets.register('app_js', app_js)
    web_assets.register('admin_css', admin_css)
    web_assets.register('admin_js', admin_js)
    web_assets.manifest = 'cache' if not app.debug else False
    web_assets.cache = not app.debug
    web_assets.debug = app.debug
