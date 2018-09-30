DEBUG = True
def dbg_init():
    global DEBUG
    if DEBUG:
        import sys
        sys.dont_write_bytecode = True
def dbg(x):
    global DEBUG
    if DEBUG:
        print(x)