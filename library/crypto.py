import string
from hashlib import pbkdf2_hmac

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes, random


def getKey(userName, mainPassword):
    # 200000 rounds of PBKDF2-SHA512
    # gets key
    key = pbkdf2_hmac('sha512', mainPassword.encode(),
                      userName.encode(), 200000, 32)
    return key


def getAuthHash(userName, mainPassword):
    # authentication hash
    authHash = pbkdf2_hmac('sha512', getKey(
        userName, mainPassword), mainPassword.encode(), 1, 32)
    return authHash


def generateIV():
    # 16 bytes for IV
    # used for AES CBC
    # get_random_bytes from pycryptodome
    IV = get_random_bytes(16)
    return IV


def encryptVault(vaultString, key):
    # encrypted vault
    data = addPad(vaultString)
    iv = generateIV()  # generate the random IV
    aes = AES.new(key, AES.MODE_CBC, iv)  # AES CBC
    encrypted = aes.encrypt(str.encode(data))
    return iv + encrypted


def decryptVault(cipherText, key):
    # decrypt vault
    iv = cipherText[:16]  # first 16 bytes of ciphertext to assign as IV
    aes = AES.new(key, AES.MODE_CBC, iv)  # AES CBC
    return unPad(aes.decrypt(cipherText[16:])).decode('utf-8')


def addPad(st):
    # add pad to the string
    Pad = st + (32 - len(st) % 32) * chr(32 - len(st) % 32)
    return Pad


def unPad(st):
    # unpad the string
    Pad = st[:-ord(st[len(st)-1:])]
    return Pad


def generatePassword(length, configOptions=[]):
    # random generated password
    # we will pass in the length that the user wants and generate the password accordingly
    lowercaseSet = string.ascii_lowercase
    uppercaseSet = string.ascii_uppercase
    numbers = string.digits
    symbols = '~!@#$%^&*()_+}{[]'
    password = list()  # initialise the password list

    for i in range(length):
        password.append(random.choice(lowercaseSet))

    if 'upper' in configOptions:
        numToReplace = int(length/5) + 1
        for i in range(numToReplace):
            replaceIndex = random.randint(0, length-1)
            password[replaceIndex] = random.choice(uppercaseSet)

    if 'digits' in configOptions:
        numToReplace = int(length/5) + 1
        for i in range(numToReplace):
            replaceIndex = random.randint(0, length-1)
            password[replaceIndex] = random.choice(numbers)

    if 'symbols' in configOptions:
        numToReplace = int(length/6) + 1
        for i in range(numToReplace):
            replaceIndex = random.randint(0, length-1)
            password[replaceIndex] = random.choice(symbols)

    return ''.join(password)
