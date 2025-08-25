from flask import current_app as app
from flask import request, jsonify, render_template
from . import db
from .models import Task
from sqlalchemy.exc import SQLAlchemyError

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks]), 200


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    task = Task(title=title, description=data.get("description", ""))
    try:
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "db error"}), 500


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json() or {}
    if "title" in data:
        title = data["title"].strip()
        if not title:
            return jsonify({"error": "title cannot be empty"}), 400
        task.title = title
    if "description" in data:
        task.description = data["description"]
    if "done" in data:
        task.done = bool(data["done"])
    try:
        db.session.commit()
        return jsonify(task.to_dict()), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "db error"}), 500


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"status": "deleted"}), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "db error"}), 500
