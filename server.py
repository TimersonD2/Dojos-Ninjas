# # added this line to import app from flask_app
# from flask_app.controllers import users
# from flask_app import app

from flask import flash, render_template, request, redirect
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja
from flask_app import app


@app.route('/')
def index():
    return redirect('/Dojos')

@app.route('/Dojos')
def dojos():
    dojos = Dojo.get_all()
    print(dojos)
    return render_template('dojo.html', all_dojos = dojos)

@app.route('/createDojo', methods=['POST'])
def createDojo():
    data = {
        "dojoname": request.form["dojoname"],
    }
    dojo_id = Dojo.save(data)
    print('The new Dojo ID is:', dojo_id)
    return redirect('/Dojos')

@app.route('/Dojos/<int:dojo_id>')
def showDojo(dojo_id):
    data = {
        "id": dojo_id
    }
    dojos = Dojo.get_dojo_with_ninjas(data)
    return render_template("showDojo.html", all_dojos = dojos)

@app.route('/Ninjas')
def ninja():
    dojos = Dojo.get_all()
    return render_template("ninja.html", all_dojos = dojos)

@app.route('/createNinja', methods=['POST'])
def createNinja():
    data = {
        "fname": request.form['first_name'],
        'lname': request.form['last_name'],
        'age': request.form['age'],
        'dojo_id': request.form['list_id']
    }
    ninja_id = Ninja.save(data)
    flash('A New Ninja was Created')
    print('The new Ninja ID is:', ninja_id)
    return redirect('/Dojos')


if __name__ == "__main__":
    app.run(debug=True)


