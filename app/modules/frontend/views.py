# -*- coding: utf-8 -*-
"""
    phwm.modules.frontend.views
    ~~~~~~~~~~~~~

    views module for the frontend
"""
from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__, template_folder="templates")


@frontend_bp.route('/')
def index():
    return render_template('frontend/index.html')
