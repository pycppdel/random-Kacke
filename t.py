l = [1, 2, 3, 4]
def gerenator():
    for el in l:
        p = []

i = [(a, b) for a in l for b in l]
print(i)
