import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'tv-planner'
app.config["MONGO_URI"] = 'mongodb://user:password1@ds125723.mlab.com:25723/tv-planner'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_programs')
def get_programs():
    return render_template("programs.html",
    programs=mongo.db.programs.find())

@app.route('/add_program')
def add_program():
    return render_template('addprogram.html',
    categories=mongo.db.categories.find())

@app.route('/insert_program', methods=['POST'])
def insert_program():
    programs = mongo.db.programs
    programs.insert_one(request.form.to_dict())
    return redirect(url_for('get_programs'))

@app.route('/edit_program/<program_id>')
def edit_program(program_id):
    the_program = mongo.db.programs.find_one({"_id": ObjectId(program_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editprogram.html', program=the_program, categories=all_categories)

@app.route('/update_program/<program_id>', methods=['POST'])
def update_program(program_id):
    programs = mongo.db.programs
    programs.update( {'_id': ObjectId(program_id)},
    {
        'program_name': request.form.get['program_name'],
        'category_name': request.form.get['category_name'],
        'program_description': request.form.get['program_description'],
        'display_name': request.form.get['display_name'],
        'date_on': request.form.get['date_on'],
        'must_watch': request.form.get['must_watch']
    })
    return redirect(url_for('get_programs'))

@app.route('/delete_program/<program_id>')
def delete_program(program_id):
    mongo.db.programs.remove({'_id': ObjectId(program_id)})
    return redirect(url_for('#programs'))

@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find())

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form['category_name']})
    return redirect(url_for('get_categories'))



@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for("get_categories"))


@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form['category_name']}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


@app.route('/new_category')
def new_category():
    return render_template('addcategory.html',
    categories=mongo.db.categories.find())

if __name__ == '__main__':
    app.run(host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=False)
