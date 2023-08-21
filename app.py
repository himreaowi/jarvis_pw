from flask import Flask, render_template, request, jsonify, redirect, url_for
import library.api
import library.crypto
import authentication
import library.usersession
import logging
import manager
import pyperclip
import addaccount as aa

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

session = None


@app.route('/', methods=['POST', 'GET'])
def login():
    return render_template('login.html', error=False, message='none')


@app.route('/data', methods=['POST', 'GET'])
def data():
    global session
    # if request.method == 'GET':
    #     return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        if request.form.get('submit_button') == 'login':
            session = authentication.login(
                request.form['username'], request.form['password'])
            if 'error' in session:
                # show browser modal stating reason
                return render_template('login.html', error=True, message=session['error'])
            else:
                print(session['session'].getAccountNames())
                return render_template('data.html', form_data=session['session'].vaultToDictionary())
        elif request.form.get('submit_button') == 'register':
            session = authentication.register(
                request.form['username'], request.form['password'])
            if 'error' in session:
                # show browser modal stating reason
                return render_template('login.html', error=True, message=session['error'])
            else:
                return render_template('data.html', form_data=session['session'].vaultToDictionary())
        elif (request.form.get("delete_button")):
            print(session['session'].getAccountNames())
            session['session'].deleteAccount(request.form['delete_button'])
            library.api.updateVault(session['session'])
            return render_template('data.html', form_data=session['session'].vaultToDictionary())
        elif (request.form.get("passwordcopy")):
            print(request.form["passwordcopy"])
            pyperclip.copy(request.form["passwordcopy"])
            return render_template('data.html', form_data=session['session'].vaultToDictionary())
    return render_template('data.html', form_data=session['session'].vaultToDictionary())


@app.route('/addaccount', methods=['POST', 'GET'])
def addaccount():
    if request.method == 'GET':
        return f"The URL /addaccount is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        return render_template('addaccount.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    # make use of global session
    global session
    if request.method == 'GET':
        return f"The URL /addaccount/add is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        if request.form.get('submit_button') == 'add':
            print(session['session'])
            output = aa.AddAccount(
                request.form['account'], request.form['username'], request.form['password'], session['session'])
            if 'error' in output:
                redirect(url_for('data'))
                return render_template('addaccount.html', error=True, message=output['error'])
            else:
                return redirect(url_for('data'))
                # return render_template('data.html', form_data=session['session'].vaultToDictionary())
        elif request.form.get('submit_button') == 'cancel':
            return redirect(url_for('data'))
            # return render_template('data.html', form_data=session['session'].vaultToDictionary())


@app.route('/editAccount', methods=['POST', 'GET'])
def editaccount():
    if request.method == 'GET':
        return f"The URL /addaccount is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        if (request.form.get('edit_button')):
            account = session['session'].getUserAccount(
                request.form['edit_button'])

            return render_template('editAccount.html', form_data=session['session'].getUserAccount(
                request.form['edit_button']))


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    # make use of global session
    global session
    if request.method == 'GET':
        return f"The URL /edit is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        if (request.form.get('save_button')):
            account = session['session'].getUserAccount(
                request.form['save_button'])
            output = manager.editSavedetails(
                account, request.form['account'], request.form['username'], request.form['password'], session['session'])
            # output = aa.AddAccount(
            #     request.form['account'], request.form['username'], request.form['password'], session['session'])
            if 'error' in output:
                return render_template('editAccount.html', error=True, message=output['error'], form_data=session['session'].getUserAccount(
                    request.form['save_button']))
            else:
                return redirect(url_for('data'))
                # return render_template('data.html', form_data=session['session'].vaultToDictionary())
        elif request.form.get('cancel_button') == 'cancel':
            return redirect(url_for('data'))
            # return render_template('data.html', form_data=session['session'].vaultToDictionary())
    else:
        return redirect(url_for('data'))
        # return render_template('data.html', form_data=session['session'].vaultToDictionary())


@app.route('/generatepassword')
def generatepassword():
    length = request.args.get('length')
    u = request.args.get('uppercase')
    s = request.args.get('symbols')
    n = request.args.get('digits')
    passwordOptions = []
    if(u == 'true'):
        passwordOptions.append('upper')
    if(s == 'true'):
        passwordOptions.append('symbols')
    if(n == 'true'):
        passwordOptions.append('digits')
    return jsonify({'password': library.crypto.generatePassword(int(length), passwordOptions)})


if __name__ == '__main__':
    library.api.initializeDatabaseConnection()
    app.run(debug=True)
