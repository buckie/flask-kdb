from flask import Flask
from flask_kdb import KDB

app = Flask(__name__)
q = KDB(app)

@app.route("/sync/<query>")
def run_query(query):
    print query
    query = query.encode('ascii')
    data = q.connection(query)
    return str(data)


if __name__ == "__main__":
    app.run('localhost', 9000, debug=True)