from flask import Flask, redirect, render_template, session, url_for, request, flash
from database import Db, setup_db
from api import api


setup_db()
app = Flask(__name__)
app.secret_key = "penguins are great"
app.register_blueprint(api, url_prefix="/api")

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
            flash("username is already taken!", "alert")
            return render_template("signup.html")
        


@app.route("/login", methods={"GET", "POST"})
def login():
    if request.method == "GET":
        if "username" not in session:
            return render_template("login.html")
        else:
            flash("you are already logged in!", "success")
            return redirect(url_for("user"))
    else:
        un = request.form["un"]
        pw = request.form["pw"]
        if Db.usernameDoesNotExistInDb(un):
            flash("account does not exist, signup first", "alert")
            return redirect(url_for("signup"))
        else:
            if Db.correctPassword(un,pw):
                session["username"] = un
                session["db_id"] = Db.getUserId(un)
                flash("sucessfully logged in!", "success")
                return redirect(url_for("user"))
            else:
                flash("wrong password", "alert")
                return redirect("login")
        
        

@app.route("/logout")
def logout():
    session.clear()
    flash("you have been sucessefully logged out", 'info')
    return redirect(url_for("login"))




@app.route("/user/", methods={"POST", "GET"})
def user():
    if request.method == "GET":
        print(session)
        if "username" not in session:
            return redirect(url_for("login"))
        else:
            return render_template("user.html", name = session["username"], todo = Db.getToDoList(session["db_id"]))

        



if __name__ == "__main__":
    app.run(debug=True )

