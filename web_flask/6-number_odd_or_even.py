#!/usr/bin/python3
"""
This script starts a Flask web application.
"""

from flask import Flask, render_template
from urllib.parse import unquote

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Display "Hello HBNB!" on the root route.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Display "HBNB" on the /hbnb route.
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Display "C " followed by the value of the text variable.
    Replace underscore _ symbols with a space.
    """
    text = unquote(text.replace('_', ' '))
    return "C {}".format(text)


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """
    Display "Python " followed by the value of the text variable.
    Replace underscore _ symbols with a space.
    """
    text = unquote(text.replace('_', ' ')) if text else 'is cool'
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """
    Display "n is a number" only if n is an integer.
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Display a HTML page only if n is an integer:
    H1 tag: "Number: n" inside the tag BODY
    """
    if isinstance(n, int):
        return render_template('6-number.html', number=n)
    else:
        return "", 404


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """
    Display a HTML page only if n is an integer:
    H1 tag: "Number: n is even|odd" inside the tag BODY
    """
    if isinstance(n, int):
        number_type = "even" if n % 2 == 0 else "odd"
        return render_template('6-number_odd_or_even.html', number=n, number_type=number_type)
    else:
        return "", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
