"""
Ampel haben
GC ist Befehl für welche Farb hat Ampel
CC Change color


"""
AmpelFarben = ["Grün", "Gelb", "Rot", "Rotgelb"]
Zustand = 0


def ErhoeheZustand():
    global Zustand
    if Zustand < 3:
        Zustand += 1
    else:
        Zustand = 0

while True:
    NutzerEingabe = input("Geben Sie GC oder CC ein: ")
    if NutzerEingabe == "GC":
        print(AmpelFarben[Zustand])
    elif NutzerEingabe == "CC":
        ErhoeheZustand()
    elif NutzerEingabe == "exit":
        break
    else:
        print("Spasti alter







































































































        ")
