import Log

def openFile(pFileName):
  try:
    f = open(pFileName, "r")
  except FileNotFoundError:
    return Log.error("FileTool", "Impossible to open File {}".format(pFileName))
  return f

def isExist(pFileName):
  try:
    f = open(pFileName, "r")
  except FileNotFoundError:
    Log.error("FileTool", "Impossible to open File {}".format(pFileName))
    return False
  return True
