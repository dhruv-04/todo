from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

tasks= []
"""
The Tasks list would contain the dictionary containing two keys
1) Title : str (what the task is about)
2) Completed: bool (whether the task is completed or not)
3) id: uuid (to be generated once the backend recevies the request) 
"""
@app.get('/')
def mainpage():
    return "Hello World", 200

@app.get("/health")
def healthCheck():
    return "Health Good.", 200

@app.post('/todos')
def createToDo():
    try:
        payload = request.get_json() #receives the json payload (converted to python dict) from the request body
        if len(payload.keys()) == 0:
            return jsonify({ "message" : "[CREATE] Request Malformed" }), 400
        id = str(uuid.uuid4())
        payload['id'] = id
        tasks.append(payload)
        return jsonify({ "message": "[CREATE] To Do created successfully and added to the database." }), 201
    except Exception as e:
        print(f"[CREATE] Error occured while adding to the database : {e}")
        return jsonify({ "message": "[CREATE] Error Occured" }), 500

@app.get('/todos')
def getAllToDos():
    try:
        return jsonify(tasks), 200
    except Exception as e:
        print(f"[GET] Error occured while fetching the todos.")
        return jsonify({ "message": f"[GET] Error occured while fetchint the todos : {e}" }), 500
    pass

@app.get('/todo/<id>')
def getById(id):
    try:
        for task in tasks:
            if task['id'] == id:
                print(f"[GET ONE] Got the to do task.")
                return jsonify(task), 200
        return jsonify({ "message" : "Id not found." }), 404
    except Exception as e:
        print(f"[GET ONE] Error fetching the task with the id.")
        return jsonify({ "message": "[GET ONE] Error fetching the task with the given id." }), 500

@app.put('/todos/<id>')
def updateToDo(id):
    try:
        payload = request.get_json()
        for task in tasks:
            if task['id'] == id:
                task['Title'] = payload['title']
                task['Completed'] = payload['Completed']
                print(f"[UPDATE] Task with the given id updated.")
                return jsonify(task), 200
        return jsonify({ "message" : "Id not found." }), 404
    except Exception as e:
        print(f"[UPDATE] Error updating the task with the id.")
        return jsonify({ "message": "[UPDATE] Error updating the task with the given id." }), 500

@app.delete("/todos/<id>")
def deleteToDo(id):
    try:
        for task in tasks:
            if task['id'] == id:
                tasks.remove(task)
                print(f"[DELETE] Task deleted.")
                return jsonify({ "message": "Task deleted." }), 200
        return jsonify({ "message" : "Id not found." }), 404
    except Exception as e:
        print(f"[DELETE] Error deleting the task.")
        return jsonify({ "message": "[DELETE] Error deleting the task." }), 500

if __name__=="__main__":
    app.run(debug=True)