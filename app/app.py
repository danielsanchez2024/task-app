from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://mongodb.docker:27017/todolist"
mongo = PyMongo(app)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = mongo.db.tasks.find()
    result = []
    for task in tasks:
        task["_id"] = str(task["_id"])  
        result.append(task)
    return jsonify(result)

@app.route("/tasks", methods=["POST"])
def add_task():
    task_data = request.get_json()
    title = task_data.get("title")
    description = task_data.get("description")
    
    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400
    
    task = {"title": title, "description": description, "completed": False}
    task_id = mongo.db.tasks.insert_one(task).inserted_id
    new_task = mongo.db.tasks.find_one({"_id": task_id})
    new_task["_id"] = str(new_task["_id"])
    return jsonify(new_task), 201

@app.route("/tasks/<task_id>/complete", methods=["PUT"])
def complete_task(task_id):
    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    if task:
        mongo.db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": {"completed": True}})
        updated_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
        updated_task["_id"] = str(updated_task["_id"])
        return jsonify(updated_task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    result = mongo.db.tasks.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count:
        return jsonify({"message": "Task deleted successfully"})
    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
