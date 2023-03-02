from app import app
from flask import flash, redirect, render_template, url_for
from werkzeug.exceptions import HTTPException


class ShownError(Exception):
    """Displayed to users, must be human-readable"""

    def __init__(self, description: str = 'Opps! Something went wrong. \nWant to try again?',
                 original_exception: Exception | None = None, display_element_id: str | None = None):
        super(ShownError, self).__init__(description)
        self.original_exception = original_exception
        self.display_element_id = display_element_id


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(HTTPException)
def errorhandler(e):
    return render_template('error.html', e=e), 403


@app.errorhandler(401)
def unauthorised(e):
    flash('Login to gain access', 'error')
    return redirect(url_for('login'))
