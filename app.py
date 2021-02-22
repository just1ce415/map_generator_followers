"""
Laboratory 3.3
The module for running the web application
"""

from flask import render_template, Flask, request
import map_generator

app = Flask(__name__)

@app.route('/')
def enter_the_nickname():
    '''
    The page with form.
    '''
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def subtimed():
    '''
    The page with map.
    '''
    nickname = request.form.get('nickname')
    if not nickname:
        return render_template('failure.html')
    if map_generator.generate_map(nickname) == 404:
        return render_template('failure.html')
    map_layout = render_template('{}custom_map.html'.format(nickname))
    return map_layout
