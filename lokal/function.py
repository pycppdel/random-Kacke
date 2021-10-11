def CharacterCounter(wort):
    if type(wort) != str:
        return
    else:
        Dict = {}
        for el in wort:
            if el in Dict:
                Dict[el] += 1
            else:
                Dict[el] = 1
    return Dict
