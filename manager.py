from library.account import account
from library.api import updateVault

def editSavedetails(item, newAccountName, newUserName, newPassword, currentsession):
    # This function edits an account in the vault
    # This works by creating a new account object and adding it to the vault
    # The vault is then updated in the database
    # The vault is encrypted using the user's key
    # The key is generated using the user's username and password
    accountNameUpdated = False
    userNameUpdated = False
    passwordUpdate = False
    currentDetails = item
    proposedChanges = item
    Error = False
    # check not empty
    ErrorMessage = ""
    if newAccountName and newUserName and newPassword:
        # check password is >8 and <64
        if len(newPassword) >= 8 and len(newPassword) <= 64:
            if newAccountName != currentDetails.name:
                if not currentsession.checkAccountExists(newAccountName):
                    proposedChanges.name = newAccountName
                    accountNameUpdated = True
                else:
                    Error = True
                    return {'error': 'This AccountName already exists'}
            if currentDetails.username != newUserName:
                proposedChanges.username = newUserName
                userNameUpdated = True
            if currentDetails.password != newPassword:
                proposedChanges.password = newPassword
                passwordUpdate = True
            if (passwordUpdate or userNameUpdated or accountNameUpdated) and Error == False:
                if accountNameUpdated:
                    item.name = proposedChanges.name
                if userNameUpdated:
                    item.username = proposedChanges.username
                if passwordUpdate:
                    item.password = proposedChanges.password
                updateVault(currentsession)
                return {'success': 'Account edited'}
            else:
                return {'error': 'Unknwon error. No changes made to vault'}

        else:
            return {'error': 'Password must be between 8 and 64 characters'}
    else:
        return {'error': 'All fields are required'}
