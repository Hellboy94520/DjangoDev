def fatal(pClass, pMessage):
    print("FATAL in {} : {}".format(pClass, pMessage))
    print("-----------------------------------------------------------------------------------------------------------")
    exit(1)
    return False

def error(pClass, pMessage):
    print("ERROR in {} : {}".format(pClass, pMessage))
    return False

def warning(pClass, pMessage):
    print("WARNING in {} : {}".format(pClass, pMessage))

def info(pMessage):
    print("INFO : {}".format(pMessage))