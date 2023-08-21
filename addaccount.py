from library.account import account
from library.api import updateVault
from library.crypto import generatePassword


def AddAccount(lnAccountName, lnUserName, lnPassword, currentsession):
    # This function adds an account to the vault
    # This works by creating a new account object and adding it to the vault
    # The vault is then updated in the database
    # The vault is encrypted using the user's key
    # The key is generated using the user's username and password
    ErrorMessage=""
    Error=False
    ANupdate=False
    #check if empty
    if lnAccountName and lnUserName and lnPassword:
        #check password is >8 and <64
        if len(lnPassword) >=8 and len(lnPassword)<=64:
            if not currentsession.checkAccountExists(lnAccountName):
                    ANupdate = True
            else:
                    Error = True
                    return {'error': 'Account name already exists'}
            if ANupdate and Error == False:
                new_account = account(lnAccountName, lnUserName,lnPassword)
                currentsession.vault.append(new_account)
                updateVault(currentsession)
                return {'success': 'Account added'}
            else:
                return {'error': 'Unknwon error. No changes made to vault'}
        else:
            return {'error': 'Password must be between 8 and 64 characters'}
    else:
        return {'error': 'All fields are required'}


