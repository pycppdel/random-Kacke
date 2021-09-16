def random_Zahl(init, shiftzahl = 8, laenge = 8):
    Ergebnis = []
    if init < 0:
        return
    for t in range(shiftzahl):
        endByte = init & 1
        init >>= 1
        init |= 128 * (endByte ^ ((init & 2) >> 1))
        Ergebnis.append(endByte)
    zahl = 0
    anfang = 7
    for el in Ergebnis:
        zahl |= 2**anfang*el
        anfang -= 1
    return zahl
