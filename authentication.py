import library.api

def login(username, password):
    # This function is to login the user
    # This works by calling the login function from the api
    # The api returns a usersession object if the login is successful
    # The usersession object is then returned
    # If the login is unsuccessful, an error message is returned
    if username and password:
        session = library.api.login(username, password)
        if session == False:
            # show a popup saying invalid username/password and render login again
            return {'error': 'Invalid username or password'}
        elif isinstance(session, library.api.usersession):
            return {'session': session}
        else:
            return {'error': 'Unknown error'}
    elif not username or not password:
        return {'error': 'Username or password not provided'}
    else:
        return {'error': 'Unknown error'}

def register(username, password):
    # This function is to register the user
    # This works by calling the register function from the api
    # The api returns a usersession object if the registration is successful
    # The usersession object is then returned
    # If the registration is unsuccessful, an error message is returned
    if username and password:
        session = library.api.createNewAccount(username, password)
        if session == False:
            return {'error': 'Username already exists'}
        elif isinstance(session, library.api.usersession):
            return {'session': session}
        else:
            return {'error': 'Unknown error'}
    elif not username or not password:
        return {'error': 'Username or password not provided'}
    else:
        return {'error': 'Unknown error'}