from flask import Flask, render_template
import mealServiceDietInfo as meal

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return render_template('index.html', lunch = lunch(20231010))

@app.route('/getlunch')
def lunch(today):
    return meal.getDietInfo(today)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
