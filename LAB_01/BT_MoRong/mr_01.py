import itertools

lst = [1, 2, 3]

permutations = list(itertools.permutations(lst))

print("Tất cả các hoán vị của [1, 2, 3] là:")

for p in permutations:
    print(p)


