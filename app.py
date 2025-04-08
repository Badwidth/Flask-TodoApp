from flask import Flask, redirect, render_template, session, url_for, request
from database import Db



app = Flask(__name__)
app.secret_key = "penguins are great"

@app.route("/")
def root():
    return redirect(url_for("home"))

@app.route("/home/")
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        pass

#signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        if "username" not in session:
            return render_template("signup.html")
        else:
            return redirect(url_for("user"))
    else:
        un = request.form["un"]
        pw = request.form["pw"]
        if Db.usernameDoesNotExistInDb(un):
            Db.addUser(un, pw)
            session["username"] = un
            session["db_id"] = Db.getUserId(un)
            return redirect(url_for("user"))
        else:
            return render_template("signup.html")
        




@app.route("/login", methods={"GET", "POST"})
def login():
    if request.method == "GET":
        if "username" not in session:
            return render_template("login.html")
        else:
            return redirect(url_for("user"))
    else:
        un = request.form["un"]
        pw = request.form["pw"]
        if Db.usernameDoesNotExistInDb(un):
            return redirect(url_for("signup"))
        else:
            if Db.correctPassword(un,pw):
                session["username"] = un
                session["db_id"] = Db.getUserId(un)
                return redirect(url_for("user"))
            else:
                return redirect("login")
        
        


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



@app.route("/user/", methods={"POST", "GET"})
def user():
    if request.method == "GET":
        print(session)
        if "username" not in session:
            return redirect(url_for("login"))
        else:
            return render_template("user.html", name = session["username"], todo = Db.getToDoList(session["db_id"]))
    else:
        task = request.form["task"]
        Db.addTask(task, session["db_id"])
        return redirect(url_for("user"))

@app.route("/api/delete", methods=["POST", "GET"])
def api_removeitem():
    if request.method == "POST":
        task_id = request.form["task_id"]
        Db.removeTask(task_id)
        return redirect(url_for("user"))

if __name__ == "__main__":
    app.run(debug=True )

