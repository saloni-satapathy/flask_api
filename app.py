from flask import Flask, jsonify,request,make_response
from flask import abort
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)


tasks = [
     {
        'id': 1,
         'title': u'Attend Webinar',
         'description': u'Webinar on Competitive Programming', 
         'done': False
     },
     {
         'id': 2,
         'title': u'Learn React',
         'description': u'Need to find a good React tutorial on the web', 
         'done': False
     },
     {
         'id': 3,
         'title': u'Complete Assignment',
         'description': u'Complete the Operating System Assignment', 
         'done': False
     },
     {
         'id': 4,
         'title': u'Work on Project',
         'description': u'Complete the project', 
         'done': False
     }
]


auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'saloni':
        return 'salonipassword'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
   
#curl -u saloni:salonipassword -i http://localhost:5000/tasks
@app.route('/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
        return jsonify({'tasks': tasks})

#curl -u saloni:salonipassword -i http://localhost:5000/tasks/2
@app.route('/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

#curl -u saloni:salonipassword -i -H "Content-Type: application/json" -X POST -d "{"""title""":"""Read a book"""}" http://localhost:5000/tasks

@app.route('/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


#curl -u saloni:salonipassword -i -H "Content-Type: application/json" -X PUT -d "{"""done""":true}" http://localhost:5000/tasks/2


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json["title"]) != str:
        abort(400)
    if 'description' in request.json and type(request.json["description"]) is not str:
        abort(400)
    if 'done' in request.json and type(request.json["done"]) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


#curl -u saloni:salonipassword -i -H "Content-Type: application/json" -X DELETE  http://localhost:5000/tasks/2
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

 
if __name__ == '__main__':
    app.run(debug=True)