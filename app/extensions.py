# -*- coding: utf-8 -*-
"""
    app.extensions
    ~~~~~~~~~~~~~~~~

    extensions module
"""
import wtforms_json
from flask_migrate import Migrate
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

# Flask-SQLAlchemy extension instance
from sqlalchemy import Index
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.ddl import CreateIndex

db = SQLAlchemy()


# Customize the DDL for MySQL to allow a FULLTEXT parameter on indexes. e.g.
# Index("idx_name", column, mysql_fulltext=True)
Index.argument_for("mysql", "fulltext", False)


@compiles(CreateIndex, "mysql")
def gen_create_index(element, compiler, **kw):
    text = compiler.visit_create_index(element, **kw)
    if element.element.dialect_options['mysql']['fulltext']:
        text = text.replace("CREATE INDEX", "CREATE FULLTEXT INDEX")
    return text


# Flask-Security extension instance
security = Security()

# Flask-Migrate extension instance
migrate = Migrate()

# JSON Support for WTForms
wtforms_json.init()
