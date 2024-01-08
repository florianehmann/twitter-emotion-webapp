"""Endpoints of the base Module"""

from flask import render_template

from app.base import bp
from app.base.forms import QueryForm
from app.base.query_page import process_user_request


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    """Main page with form to request classifications"""

    form = QueryForm()
    common_kwargs = {'form': form}

    render = None
    if form.validate_on_submit():
        render = process_user_request(form, common_kwargs)

    if render is None:
        render = render_template('base/index.html', **common_kwargs)

    return render


@bp.route('/privacy')
def privacy():
    """Privacy statement of the site"""
    return render_template('base/privacy.html')
