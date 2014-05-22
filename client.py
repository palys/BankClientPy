import sys, traceback, Ice
import Bank

ic = None
manager = None
account = None

def newAccount():
	name = raw_input("Podaj imie\n")
	lastName = raw_input("Podaj nazwisko\n")
	personalID = raw_input("Podaj pesel\n")
	data = Bank.PersonalData(name, lastName, personalID)
	accountType = raw_input("Podaj typ konta\n[s] - silver\n[p] - premium\n")
	type = None
	if (accountType == "s"):
		type = Bank.accountType.SILVER
	else:
		type = Bank.accountType.PREMIUM
	ID = manager.createAccount(data, type)
	print ID
	if (accountType == "s"):
		inSilver()
	else:
		inPremium()
	
def existnigSilver():
	ID = raw_input("Podaj id\n")
	account = Bank.AccountPrx.checkedCast(ic.stringToProxy("silver/" + ID + ":tcp -p 10000"))
	inSilver(account)
	
def existingPremium():
	ID = raw_input("Podaj id\n")
	account = Bank.PremiumAccountPrx.checkedCast(ic.stringToProxy("premium/" + ID + ":tcp -p 10000"))
	inPremium(account)
	
def inSilver(account):
	c = raw_input("[t] - transfer\n[a] - stan konta\n[w] - wyjscie")
	if c == "t":
		amount = raw_input("Podaj kwote\n")
		to = raw_input("Podaj id docelowe\n")
		account.transfer(to, int(amount))
	elif c == "a":
		print account.getBalance()
	elif c == "w":
		exit()
	else:
		print "Niepoprawna komenda"
	inSilver(account)
	
def inPremium(account):
	c = raw_input("[t] - transfer\n[a] - stan konta\n[w] - wyjscie")
	if c == "t":
		amount = raw_input("Podaj kwote\n")
		to = raw_input("Podaj id docelowe\n")
		account.transfer(to, int(amount))
	elif c == "a":
		print account.getBalance()
	elif c == "w":
		exit()
	else:
		print "Niepoprawna komenda"
	inPremium(account)
	
def exit():
	if ic:
	# Clean up
		try:
			ic.destroy()
		except:
			traceback.print_exc()
			status = 1

	sys.exit(status)

status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    base = ic.stringToProxy("manager/1:tcp -p 10000")
    manager = Bank.BankManagerPrx.checkedCast(base)
    if not manager:
        raise RuntimeError("Invalid proxy")
        
        
    s = raw_input("[n] - nowe konto\n[s] - istniejace konto zwykle\n[p] - istniejace konto premium\n[w] - wyjscie\n")
    
    if s == "n":
        newAccount()
    elif s == "s":
        existnigSilver()
    elif s == "p":
        existingPremium()
    elif s == "w":
        exit()
    
    

except:
    traceback.print_exc()
    status = 1

if ic:
    # Clean up
    try:
        ic.destroy()
    except:
        traceback.print_exc()
        status = 1

sys.exit(status)
