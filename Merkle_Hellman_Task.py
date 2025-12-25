
import random #for random generation
import math # for gcd calculation
import ast # for readng user input as a list

# ------------------------------------- Number Sequence e ------------------------------------------- #

# function takes in the required length of the sequence
# max jump is the maximum increase between each number in the sequence
def makeRandomSeq(length):

    # for making sure the next number is greater than the combined total of all those before it
    total = 0

    #for storing the output
    seq = []

    # max jump is the maximum increase between each number in the sequence
    maxJump = 10

    #loop length amount of times
    for count in range(length):

        # generates the next number between the total of all the previous
        # numbers plus one and the total plus the maximum jump so that the next
        # number cannot be the same as the total or randomly large
        nextNum = total + random.randint(1,maxJump)

        #updates the total to include the new number
        total += nextNum

        # adds the new number to the sequence list
        seq.append(nextNum)

    return seq

# ------------------------------------- ^ Number Sequence e ^ ------------------------------------------- #

# ------------------------------------- Prime Number q ------------------------------------------- #

# HELPER FOR CHECKING IF NUM IS PRIME
def isPrime(num):

    isP = True

    # n**0.5 is the squareroot of n / n to the power of 0.5
    #this checks if the number is divisable up to it's sqrt
    for i in range(2, int(num**0.5) +1):

        # checks the remainder
        #it cant be prime if there is a remainder
        if num % i == 0:
            isP = False
            break

    #print(num, "is prime =", isP)
    return isP
    

# For finding a prime number between 23 and primeMax
def getPrime(primeMax):

    #print("\nfinding prime...")

    # generate a random number up to the primeMax
    possPrime = random.randint(0,primeMax)
    #print(possPrime)
    
    #check if it is prime and regenerate until it is
    while isPrime(possPrime) != True:
        possPrime = random.randint(0,primeMax)
        #print(possPrime)
        
    #print("prime found -", possPrime)
    
    return possPrime


def selectValidPrime(seq, primeMax):

    #print("\nFinding valid prime number for sequence")

    #generate a prime number
    possibleP = getPrime(primeMax)

    # checks if the last number in the sequence is double
    #or greater the size of the prime number
    while possibleP <= (seq[-1]*2):

        # if not then regenerate prime numbers until it is
        possibleP = getPrime(primeMax)

    #print("Valid prime =", possibleP)

    return possibleP
    

# ----------------------------------- ^ Prime Number q ^ --------------------------------------------- #

# ----------------------------------- CoPrime Number w --------------------------------------------- #

def GetCoPrime(q):
    # generate a coprime for q
    found = False

    # loop until coprime is found
    while found != True:

        #generate random possible coprime
        w = random.randint(2, q-1)

        # check if they only share 1 as a gcd
        if math.gcd(w, q) == 1:
            found = True
            
    return w

# ----------------------------------- ^ CoPrime Number w ^ ----------------------------------------- #

# ----------------------------------- Public Key h --------------------------------------------- #

def CalcPublicKey(e,q,w):

    pubKey = []

    # for each e value
    for e in e:
        # add ee to the public key list, as per the spec
        pubKey.append( (e*w) % q )

    #print(pubKey)
    return pubKey

# ----------------------------------- ^ Public Key h ^ --------------------------------------------- #


def CreateBlocks(bits, size):

    # list for split up binary
    blocks = []

    # loop for the length of bits, incrementing by the block size
    for i in range(0, len(bits), size):

        # add the block size amount of bits to the new list
        blocks.append(bits[i:i+size])

    return blocks


# ----------------------------------- Message Encryption  --------------------------------------------- #

def MssgToBinary(mssg):

    # list of characters
    lMssg = list(mssg)
    # for the binary values of the char
    bMssg = []
    #print(lMssg)

    # final list for storing each binary character
    binaryM = []

    # changes each character to ascii value
    for x in range(len(lMssg)):
        lMssg[x] = ord(lMssg[x])
        #print(lMssg)

        #bin() changes the value to binary
        #[2:] takes away the prefix that bin() automatically adds
        # .zfill(8) makes sure that 
        bMssg.append( bin(lMssg[x])[2:].zfill(8) )

    #print(bMssg)

    # format the words from binary strings to single 0s or 1s in the list
    for x in bMssg:
        for y in x:
            binaryM.append(int(y))

    #print("Message =", mssg)          
    #print("Binary of message =",binaryM)

    return binaryM



def EncryptBlockMssg(mssg, key):

    # for storing total ciphertext value
    cipher = 0
    #for counting characters
    charCounter = 0

    # for each bit in the binary mssg list
    for b in mssg:

        # multiply the bit by the block key value
        bVal = b * key[charCounter]

        # add the value to the running total
        cipher += bVal

        #i increment the bit counter by 1
        charCounter += 1

    return cipher

# ----------------------------------- ^ Message Encryption ^ --------------------------------------------- #


# ----------------------------------- Message Decryption --------------------------------------------- #

def DecryptBlockMssg(eSum, seq, valPrime, coPrime):

    # calculate modular inverse
    modInv = pow(coPrime, -1, valPrime)
    #print("modular inverse=",modInv)

    # calculate the decrypted sum
    dSum = (eSum * modInv) % valPrime
    #print("Decryption sum = ",dSum)


    #list of decoded bits 
    dBits = []

    #loop backwards through the sequence to start with the largest value
    for val in reversed(seq):

        # if the value is smaller or equal to the decryption sum
        if val <= dSum:
            #the bit must be a 1
            dBits.append(1)
            #subtract the current value from the sum
            dSum -= val
        else:
            # otherwise the value must be a 0
            dBits.append(0)

    # reverse the list back to the right way round as the values were calculated backwards
    dBits.reverse()

    return dBits

    

def BinaryToText(binMssg):

    #for binary->ascii
    asciiTrans = []
    #for ascii->text
    txtTrans = []

    # while there is something in the list
    while len(binMssg) != 0:

        #start the total at 8
        #and the add amount at 128, as each letter is maximum 8 bits
        letterTot = 0
        addAmount = 128

        # loop 8 times as each letter is contained in 8 bits
        for y in range(8):

            #if the bit is a 1 then add the addAmount to the total
            if int(binMssg[y]) == 1:
                letterTot += addAmount

            # otherwise half the addAmount and loop again
            addAmount //= 2

        #add the value to the ascii list
        asciiTrans.append(letterTot)

        # take the translated bits out
        binMssg = binMssg[8:]

    # then for each number in the list
    for y in range(len(asciiTrans)):
        #change it from ascii to text and add it to the text list
        txtTrans.append(chr(asciiTrans[y]))

    # once all the binary is translated, change the list to a string, like was encrypted
    txtTrans = "".join(txtTrans)

    return txtTrans


# ----------------------------------- ^ Message Decryption ^ --------------------------------------------- #


# --------------------------- MAIN -------------------------------- #

# In the spec this is how the following are refferred to:
# sequence = e
# selectValidPrime = q
# coPrime = w
# publicKey = h

## blockSeqLen of 64 requires at least a max of 10 * pow(10,20) - takes a long while
## blockSeqLen of 56 requires at least a max of 10 * pow(10,18) - 19 wb. but takes time
## blockSeqLen of 48 requires at least a max of 10 * pow(10,14) - 15 works better
## blockSeqLen of 40 requires at least a max of 10 * pow(10,13) - RECCOMENDED
## blockSeqLen of 32 requires at least a max of 10 * pow(10,10)
## blockSeqLen of 24 requires at least a max of 10 * pow(10,7)
## blockSeqLen of 16 requires at least a max of 10 * pow(10,5)


def mainProg():

    print("\n- - - - Options - - - -")
    print("f  = full key generation with a preset 500 characters plus encryption and decryption")
    print("c  = choose text to encrypt and decrypt with generated keys")
    print("d  = decrypt ciphertext using given values")
    print("g  = just generate public and private keys")
    print("q  = Exit program\n\n")

    userIn = str(input("$ "))

    match userIn:

        ## This case gives uses the 500 char message, as required in the spec
        ## It generates a public and private key and encrypts and decrypts the message
        ## No user input required
        case "f":
            char500Mssg = "silverMoonPathCrystalRiverEchoBrightCanyonLightHiddenValleyRoadAmberForestWingGentleHarborStoneRisingMeadowCallGoldenCedarLineRapidHorizonFlowQuietPrairieMarkSilentTimberShadeWanderingStarPulseAutumnForestGateMorningBreezeRunFrozenPineDriftOpenHarborTrailWildRidgeMotionSkywardFlowerStepCrimsonShadowRiseDistantCanyonDriftNobleMeadowSparkTrueRiverGuideLoneSummitWindSoftCedarDreamVividHorizonLift"
            blockSeqLen = 40
            blockPrimeMax = 10 * pow(10,13)

            print("Message to be used: ", char500Mssg)

            e = makeRandomSeq(blockSeqLen)

            ranQ = random.randint((e[-1]*2)+1, blockPrimeMax)
            q = selectValidPrime(e, ranQ)
            w = GetCoPrime(q)
            h = CalcPublicKey(e, q, w)

            #format the private key
            pk = []
            pk.append(e)
            pk.append(q)
            pk.append(w)

            #print key values for user
            print("\n- - - - - Public Key - - - - -")
            print(h)
            print("\n- - - - - Private Key - - - - -")
            print(pk)

            print("\n\n----------------------- Encrypting ------------------------------")
            binMssg = MssgToBinary(char500Mssg)
            blocks = CreateBlocks(binMssg, blockSeqLen)
            cipherVal = [EncryptBlockMssg(block, h) for block in blocks]
            print("Encrypted message value =", cipherVal)

            print("\n\n----------------------- Decrypting ------------------------------")
            dBlocks = [DecryptBlockMssg(c, e, q, w) for c in cipherVal]
            dMssg = [bit for block in dBlocks for bit in block]
            outputMssg = BinaryToText(dMssg)
            print("Decrypted Message =", outputMssg)


        ## This is the same as "f" except it takes in the user's message to be used
        case "c":
            print("Enter text to be encrypted and decrypted")
            userMssg = str(input("$ "))
            
            
            blockSeqLen = 40
            blockPrimeMax = 10 * pow(10,13)

            e = makeRandomSeq(blockSeqLen)

            ranQ = random.randint((e[-1]*2)+1, blockPrimeMax)
            q = selectValidPrime(e, ranQ)
            w = GetCoPrime(q)
            h = CalcPublicKey(e, q, w)

            #format the private key
            pk = []
            pk.append(e)
            pk.append(q)
            pk.append(w)

            #print key values for user
            print("\n- - - - - Public Key - - - - -")
            print(h)
            print("\n- - - - - Private Key - - - - -")
            print(pk)

            print("\n\n----------------------- Encrypting ------------------------------")
            binMssg = MssgToBinary(userMssg)
            blocks = CreateBlocks(binMssg, blockSeqLen)
            cipherVal = [EncryptBlockMssg(block, h) for block in blocks]
            print("Encrypted message value =", cipherVal)

            print("\n\n----------------------- Decrypting ------------------------------")
            dBlocks = [DecryptBlockMssg(c, e, q, w) for c in cipherVal]
            dMssg = [bit for block in dBlocks for bit in block]
            outputMssg = BinaryToText(dMssg)
            print("Decrypted Message =", outputMssg)

        case "d":
            print("Enter the ciphertext in the list format: ")
            userCInput = input("$ ")
            userCInput = ast.literal_eval(userCInput) #converts string to type that user entered
            if not(type(userCInput) is list): #checks if user entered a list
                print("Wrong input type")
                print("======== Program Ended ========")
                return

            print("Enter private key in list format [e,q,w]:")
            userPKInput = input("$ ")
            userPKInput = ast.literal_eval(userPKInput) #converts string to type that user entered
            if not(type(userCInput) is list): #checks if user entered a list
                print("Wrong input type")
                print("======== Program Ended ========")
                return

            e, q, w = userPKInput
            
            
            print("\n\n----------------------- Decrypting ------------------------------")
            dBlocks = [DecryptBlockMssg(c, e, q, w) for c in userCInput]
            dMssg = [bit for block in dBlocks for bit in block]
            outputMssg = BinaryToText(dMssg)
            print("Decrypted Message =", outputMssg)


        case "g":
            
            blockSeqLen = 40
            blockPrimeMax = 10 * pow(10,13)

            e = makeRandomSeq(blockSeqLen)

            ranQ = random.randint((e[-1]*2)+1, blockPrimeMax)
            q = selectValidPrime(e, ranQ)
            w = GetCoPrime(q)
            h = CalcPublicKey(e, q, w)

            # create private key list and add e, q, w as per the spec
            pk = []
            pk.append(e)
            pk.append(q)
            pk.append(w)

            #print key values for user
            print("\n- - - - - Public Key - - - - -")
            print(h)
            print("\n- - - - - Private Key - - - - -")
            print(pk)

        case "q":
            exit()

        # for catching invalid inputs
        case _:
            print("= = = = = Invalid Input = = = = =")
            mainProg()


# loops the program until the users says they are done
mainProg()
done = input("Done? (y/n)")
while done == "n":
    mainProg()
    done = input("Done? (y/n)")
