import pprint as pp

lista = [
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [3, 4, 5, 6],
    [7, 8, 6, 4]
]

t1 = [1, 2, 3, 4]
t2 = [3, 4, 5, 6]

pp.pprint(lista)

zipped = list(zip(*[elem for elem in lista]))
zipped2 = list(zip(t1, t2))


pp.pprint(zipped)
pp.pprint(zipped2)
