from flask import Flask, render_template , request,redirect
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
project_path = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_path,"my_database.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app) 


class Expense(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String,nullable=False)
    expensename = db.Column(db.String,nullable=False)
    amount = db.Column(db.Integer,nullable=False)
    category = db.Column(db.String,nullable=False)



@app.route('/')
def add():
    return render_template('add.html')

@app.route('/expenses')
def expenses():
    expenses = Expense.query.all()
    total,t_food,t_utilities,t_entertainment,t_travel,t_others =0,0,0,0,0,0
    for expense in expenses:
        total+=expense.amount
        if expense.category=="Food":
            t_food+=expense.amount
        elif expense.category=="Utilities":
            t_utilities+=expense.amount
        elif expense.category == "Entertainment":
            t_entertainment+=expense.amount
        elif expense.category == "Travel":
            t_travel+=expense.amount
        else:
            t_others+=expense.amount

    return render_template('expenses.html',expenses=expenses,total=total,t_food=t_food,
                           t_utilities=t_utilities,t_entertainment=t_entertainment,t_travel=t_travel,
                           t_others=t_others)

@app.route('/delete/<int:id>')
def delete(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect("/expenses")

@app.route('/expenses/<int:id>')
def edit(id):
    expense = Expense.query.filter_by(id=id).first()
    return render_template('edit.html',expense=expense)
    
@app.route('/expenses/<int:id>',methods=['POST'])
def updateexpense(id):
    expense = Expense.query.filter_by(id=id).first()
    expense.date = request.form['date']
    expense.amount = request.form['amount']
    expense.category = request.form['category']
    expense.expensename=request.form['expensename']
    db.session.commit()
    return redirect("/expenses")


@app.route('/addexpense',methods=['POST'])
def addexpense():
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    category = request.form['category']
    print (expensename)
    expense = Expense(date=date,expensename=expensename,amount=amount,category=category)
    db.session.add(expense)
    db.session.commit()
    return redirect("/expenses")


if __name__=="__main__":
    app.run(debug=True)