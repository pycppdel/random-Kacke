class Ehrenmann:
    def __init__(self, Ihrlenwert):
        self.Ihrlenwert = Ihrlenwert

    def getBezeichner(self):
        print('Ehrenmann')

class Hoernig(Ehrenmann):
    def __init__(self, straeublichkeit):
        self.__straeublichkeit = straeublichkeit
        super().__init__

class Straub(Ehrenmann):

    max_Straubwert = 100

    @staticmethod
    def IhrlenBerechnung():
        print("a * 400")


    def __init__(self, straeublichkeit):
        self.straeublichkeit = straeublichkeit
        super().__init__(self.changetoIhrle())
        setattr(self, "Hund", True)

    def getstraeublichkeit(self):
        print(self.straeublichkeit)

    def changetoIhrle(self):
        Ihrlen = self.straeublichkeit * 400
        return Ihrlen

    def getBezeichner(self):
        print("Straub")

    @property
    def straeublichkeit(self):
        print("IHRLER")
        return self.__straeublichkeit

    @straeublichkeit.setter
    def straeublichkeit(self, value):
        if value>0:
            self.__straeublichkeit = value
        else:
            pass

    def __del__(self):
        print("LASS MICH LEBEN")

    def __str__(self):
        return "Kuchen"

    def __lt__(self, other):
        back = self.straeublichkeit < other.straeublichkeit
        return back




Straub1 = Straub(30)
Straub2 = Straub(100)
print(Straub1 < Straub2)
