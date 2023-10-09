from flask import Flask, render_template
from getLunch import getLunch

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return render_template('index.html', lunch = getLunch(20230913))

@app.route('/getlunch')
def lunch(today):
    return getLunch(today)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)