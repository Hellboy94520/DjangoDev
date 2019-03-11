""" Fonction permettant de mettre la première lettre de chaque mot en lettre capitale et le reste en minuscule """
def adjustLowerAndUpperText(pString):
  # On sépare chaque mot
  lWordList = pString.split(" ")
  # On créé notre nouveau string
  lNewWord = ""
  for i, word in enumerate(lWordList):
    if i == 0:
      lNewWord = word[:1]+word[1:].lower()
    else:
      lNewWord += " " + word[:1]+word[1:].lower()

  return lNewWord
