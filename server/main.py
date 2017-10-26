from flask import Flask, request
from secret import problems
import os
import json

app = Flask(__name__)
@app.route('/')
def index():
    return open('index.html').read()

@app.route('/index.js')
def indexjs():
    return open('index.js').read()

@app.route('/problems/')
def ret_problems():
    return json.dumps({'problems': [{'statement': problem['statement']} for
        problem in problems]})

def write_name(problem, name):
    filename = "solvers%d" % problem
    with open(filename, 'a') as f:
        f.write(name + '\n')


def get_names(problem):
    filename = "solvers%d" % problem
    with open(filename, 'r') as f:
        ret = f.read().strip('\n').split('\n')
    return ret


def validate(problem):
    try:
        p = int(problem)
    except:
        return -1
    if p < 0 or p >= len(problems):
        return -1
    return p


@app.route('/problems/<path:path>', methods = ['POST', 'GET'])
def problem(path):
    p = validate(path)
    if p == -1:
        return '{"Status": 2, "Error": "problem_id error"}'
    if request.method == 'POST':
        print(request.form)
        if problems[p]['flag'] == request.form['flag']:
            write_name(p, request.form['name'])
            return '{"Status": 1}'
        else:
            return '{"Status": 3, "Error": "Wrong Answer."}'

    d = {'solvers': get_names(p), 'score': problems[p]['score']}
    return json.dumps(d)

port = int(os.environ.get('PORT', 8080))
app.run(port=port, host='0.0.0.0')

