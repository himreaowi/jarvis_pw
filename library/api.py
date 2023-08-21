import base64
import json

import pyrebase

from library.crypto import decryptVault, encryptVault, getAuthHash, getKey
from library.usersession import usersession


def getConfig():
    # This is a function to get the config for firebase
    # This is to prevent the config from being exposed
    config = {"apiKey": "AIzaSyCcdNC18e2HGMLuWMWk9f78Nalkv0lM43k",
              "authDomain": "password-manager-f6d9c.firebaseapp.com",
              "databaseURL": "https://password-manager-f6d9c-default-rtdb.europe-west1.firebasedatabase.app",
              "projectId": "password-manager-f6d9c",
              "storageBucket": "password-manager-f6d9c.appspot.com",
              "messagingSenderId": "197187861509",
              "appId": "1:197187861509:web:70ae9f6dc76ad1e246306c",
              "measurementId": "G-BDP19VMP24"}
    return config


def initializeDatabaseConnection():
    # This function is to initialize the database connection
    firebase = pyrebase.initialize_app(config=getConfig())
    global db
    db = firebase.database()


def login(username, password):
    # This function is to login to the database
    # This works by getting the user's authHash from the database
    # and comparing it with the authHash generated from the password
    # If the authHash matches, the user is logged in
    # If the authHash does not match, the user is not logged in
    authHash = getAuthHash(username, password)
    dbAuthHash = str(db.child("CZ4010DB").child(
        "users").child(username).child('authHash').get().val())

    # This is to decode the authHash from the database
    if dbAuthHash == base64.b64encode(authHash).decode():
        cipher = base64.b64decode(str(db.child("CZ4010DB").child(
            "users").child(username).child('vault').get().val()))

        lock = db.child("CZ4010DB").child("users").child(
            username).child('lock').get().val()
        clipboard = db.child("CZ4010DB").child("users").child(
            username).child('clipboard').get().val()

        key = getKey(username, password)

        # decrypt the vault
        vaultStrings = decryptVault(cipher, key)
        vaultDictionary = json.loads(vaultStrings)
        session = usersession(username, authHash, key, clipboard, lock)
        session.clearVault()
        session.dictionaryToVault(vaultDictionary)

        # return the session
        return session
    else:
        return False


def createNewAccount(username, password):
    # This function is to create a new account
    # This works by creating a new user in the database
    # and adding the user's authHash to the database
    authHash = getAuthHash(username, password)
    snapshot = db.child("CZ4010DB").child("users").child(username)
    if str(snapshot.child('userName').get().val()) == username:
        return False
    else:
        key = getKey(username, password)
        vault = []
        session = usersession(username, authHash, key, 5000, 0, vault)
        updateVault(session)
        return session


def updateVault(session):
    # This function is to update the vault in the database
    # This works by encrypting the vault and adding it to the database
    # The vault is encrypted using the user's key
    # The key is generated using the user's username and password
    snapshot = db.child("CZ4010DB").child("users").child(session.userName)
    vaultDict = session.vaultToDictionary()
    encryptedVault = encryptVault(json.dumps(vaultDict), session.key)
    body = {
        'userName': session.userName,
        'authHash': base64.b64encode(session.authHash).decode(),
        'clipboard': session.clipboard,
        'lock': session.lock,
        'vault': base64.b64encode(encryptedVault).decode(),
    }
    snapshot.update(body)
