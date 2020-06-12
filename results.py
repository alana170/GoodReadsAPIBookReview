from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('forms.html')

@app.route('/', method = ['POST'])
def getValues():
    name = request.form['fname']
    age = request.form['lname']
    db = request.form['q1']
    return render_template('action_page.html', n = name, age = age, db =db)



if __name__=='__main__' :
    app.run(debug=True)


