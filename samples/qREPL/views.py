from flask import render_template, request, redirect, session, flash
from qpython.qtype import QException

from flask_kdb import get_kdb
from flask_kdb.utils import get_q_status, convert_qdata
from . import app


@app.before_first_request
def set_query():
    session['query'] = None


@app.route("/", methods=['GET'])
def display_ide():
    q_conn = get_kdb()
    qstatus = get_q_status(q_conn)
    if session['query']:
        return render_template('query.html', **session['query'])
    else:
        session['query'] = None
        return render_template('base.html', qstatus=qstatus, orig_query=None)


@app.route("/run_query", methods=['POST'])
def run_query():
    q_conn = get_kdb()
    qstatus = get_q_status(q_conn)
    orig_query = request.form['queryText']
    if 'stripNewline' in request.form:
        stripNewline = True
    else:
        stripNewline = False
    errors = False
    if stripNewline:
        query = orig_query.encode('ascii').replace('\n', ' ').replace('\r', '').replace('  ', ' ')
        try:
            data = q_conn(query)
        except QException as e:
            errors = True
            flash(str(e), 'qerror')
    else:
        queries = [i for i in orig_query.encode('ascii').splitlines()]
        for query in queries:
            try:
                data = q_conn(query)
            except QException as e:
                errors = True
                flash(str(e), 'qerror')

    if not errors:
        data = convert_qdata(data)
        session['query'] = dict(qstatus=qstatus, orig_query=orig_query, query=query, query_result=data)
    return redirect('/')



