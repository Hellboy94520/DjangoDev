import Log

def openFile(pFileName):
  try:
    f = open(pFileName, "r")
  except FileNotFoundError:
    return Log.error("FileTool", "Impossible to open File {}".format(pFileName))
  return f