"""
User wird nach einem File gefragt
File wird zwischengespeichert
CodeAbschnitt 1 beginnt
Nach Nutzereingaben fragen
Nutzereingaben speichern
Nachdem der Nutzer eine Angabe gemacht hat, dass er nicht mehr
eigeben will endet das Program
Codeabschnitt 2
Datei wird geöffnet alles was gespeichert ist wird reingeschrieben
"""

Desktopweg = "/home/paul/Schreibtisch/"
UserDatei = input("In wie soll Ihr File heißen? Beenden mit leave(): ")

while UserDatei != "leave()":
    Datei = open(Desktopweg + UserDatei + ".txt", "w")
    UserDateiInhalt = input("Was wollen Sie in " + UserDatei + " schreiben? Beenden mit leave(): ")
    if UserDateiInhalt != "leave()":
        Datei.write(UserDateiInhalt)
        if UserDateiInhalt
        Datei.close()

    else:
        break
