from library.account import account


class usersession(object):

    def __init__(self, userName, authHash, key, clipboard, lock, vault=[]):
        # This is the constructor for the usersession class
        # This class is used to store the user's session
        # This includes the user's username, authHash, key, clipboard, lock and vault
        self.userName = userName
        self.authHash = authHash
        self.key = key
        self.vault = vault
        self.lock = lock
        self.clipboard = clipboard

    def clearVault(self):
        # Initialize the vault to an empty list of accounts
        self.vault = []

    def getUserAccount(self, name):
        # This function is to get the account from the vault
        # This works by looping through the vault and returning the account with the same name
        account = next((a for a in self.vault if a.name == name), None)
        return account

    def checkAccountExists(self, name):
        # This function is to check if the account exists in the vault
        # This works by looping through the vault and checking if the account exists
        account = name in self.getAccountNames()
        return account

    def getAccountNames(self):
        # This function is to get the names of all the accounts in the vault
        # This works by looping through the vault and adding the names to a list
        accountNames = sorted([a.name for a in self.vault])
        return accountNames

    def deleteAccount(self, name):
        # This function is to delete an account from the vault
        # This works by looping through the vault and deleting the account with the same name
        self.vault.remove(self.getUserAccount(name))

    def vaultToDictionary(self):
        # This function is to convert the vault to a dictionary
        # This works by looping through the vault and adding the accounts to a list
        dictionary = [a.__dict__ for a in self.vault]
        return dictionary

    def dictionaryToVault(self, dictionary):
        # This function is to convert the dictionary to a vault
        # This works by looping through the dictionary and adding the accounts to the vault
        for x in dictionary:
            self.vault.append(account(x['name'], x['username'], x['password']))
