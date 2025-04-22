from flask import Blueprint, redirect, render_template, session, url_for, request
from database import Db
api = Blueprint("api", __name__, template_folder="templates")

@api.route("/delete", methods=["POST", "GET"])
def api_removeitem():
    if request.method == "POST":
        task_id = request.form["task_id"]
        Db.removeTask(task_id)
        return redirect(url_for("user"))

@api.route("/add", methods=["POST", "GET"])
def api_additem():
    if request.method == "POST":
        task = request.form["task"]
        Db.addTask(task, session["db_id"])
        return redirect(url_for("user"))