from flask import Flask, jsonify

app = Flask(__name__)


def sum(x, y):
    return x + y

def div(x, y):
    return x / y



@app.route('/sum/div/<int:n1>/<int:n2>')
def sum_route(n1, n2):
    re = {
        "sum": sum(n1, n2),
        "div": div(n1,n2),
        "server IP": "12.233.4.3"

    }
    return jsonify(re)

if __name__ == '__main__':
    app.run(debug=True)
