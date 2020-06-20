from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('forms.html')

"""
@app.route('/', method = ['POST'])
def getValue():
    name = request.form['name']
    age = request.form['age']
    db = request.form['dateofbirth']
    return render_template('action_page.html', n = name, age = age, db =db)
"""

if __name__=='__main__' :
    app.run(debug=True)


