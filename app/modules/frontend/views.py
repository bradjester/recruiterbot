# -*- coding: utf-8 -*-
"""
    phwm.modules.frontend.views
    ~~~~~~~~~~~~~

    views module for the frontend
"""
from flask import Blueprint, url_for, redirect
from flask_security import current_user, url_for_security
frontend_bp = Blueprint('frontend', __name__, template_folder="templates")


@frontend_bp.route('/')
def index():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.index'))
    elif current_user.is_authenticated:
        return redirect(url_for('job.index'))
    else:
        return redirect(url_for_security('login'))
