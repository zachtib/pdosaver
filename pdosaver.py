import logging
import sys
from flask import Flask, render_template

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def home():
    app.logger.debug('Hello, World!')
    return render_template('base.html')
