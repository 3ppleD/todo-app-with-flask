from flask import Blueprint, session, redirect, flash, url_for, request, render_template
from model.model import Todo
from _init_ import db
from functools import wraps


todo_bp = Blueprint("todo_bp", __name__)
# check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to access this page', 'warning')
            return redirect(url_for('user_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

@todo_bp.route("/homepage", methods = ['GET', 'POST'])
# check if logged in
@login_required
def homepage():
    # get user id and name from session
    user_id = session['user_id']   
    name = session['name']
# filter by id to get a particular user    
    todo = Todo.query.filter_by(userId = user_id).all()

#Getting inputs from the html    
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

#check if title is not inputed
        if not title:
            flash("Title is required", "error")
        else:
            # add inputs to the database for todo
            new_todo = Todo(name = title, description = description, userId = user_id)
            db.session.add(new_todo)
            db.session.commit()
            flash("Task successfully added", "success")
            return redirect(url_for("todo_bp.homepage"))
    return render_template("Todo.html", todo = todo, name = name)  


@todo_bp.route("/complete_task/<int:todo_id>", methods = ['POST'])
#check if logged in
@login_required
def completed_task(todo_id):
    #check if id is present and returns 404 if not present
    todo  = Todo.query.get_or_404(todo_id)


#check if user_id in the databas matches what is in the session

    if todo.userId != session.get("user_id"):
        flash("You don't have permission to update this task", "error")
        return redirect(url_for("todo_bp.homepage"))
    
    #update iscompleted to True

    todo.iscompleted = True
    db.session.commit()

    flash("Task marked as completed", "success")
    return redirect(url_for("todo_bp.homepage"))

# deleting the todo list

@todo_bp.route("/deleteOne/<int:todo_id>")
@login_required
def deleteOne(todo_id):
      deleteOneTodo = Todo.query.get_or_404(todo_id)

      db.session.delete(deleteOneTodo)
      db.session.commit()

      flash("Task deleted successfully")
      return redirect(url_for("todo_bp.homepage"))


@todo_bp.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    # flash('You have been logged out.', 'success')
    return redirect(url_for('user_bp.login'))