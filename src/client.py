import sys, traceback, Ice
import generated.Bank_ice

status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    base = ic.stringToProxy("manager/1:tcp -p 10000")
    manager = Bank_ice.BankManagerPrx.checkedCast(base)
    if not manager:
        raise RuntimeError("Invalid proxy")

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
