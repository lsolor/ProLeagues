
import os
# accessible as a variable in index.html in template
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


DATABASEURI = "postgresql://postgres:Cleanslate25@35.243.220.243/proj1part2"


engine = create_engine(DATABASEURI)



@app.before_request
def before_request():

    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback;
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):

    try:
        g.conn.close()
    except Exception as e:
        pass


@app.route('/')
def index():
    print(request.args)

    #
    # example of a database query
    #
    # cursor = g.conn.execute("SELECT name FROM test")
    # names = []
    # for result in cursor:
    #     names.append(result['name'])  # can also be accessed using result[0]
    # cursor.close()
    #
    # context = dict(data=names)

    return render_template("index.html" )#**context)


@app.route('/another')
def another():
    return render_template("another.html")


@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
    return redirect('/')


@app.route('/login')
def login():
    #abort(401)
    #this_is_never_executed()
    return 0

if __name__ == "__main__":
    import click


    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):


        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()



