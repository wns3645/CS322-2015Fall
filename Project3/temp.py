__author__ = 'Junhui'


r = list()

for i in range(0, 68):
    a = input()

    a = a.split(' => ')

    a[1] = int(a[1])

    k = a[0][1]
    b = a[0][5]

    a[0] = []

    a[0].append(int(k))
    a[0].append(b)

    r.append(a)

for i in range(69, 116):

    a = input()

    a = a.split(' => ')

    a[1] = int(a[1])

    k = a[0][1] + a[0][2]
    b = a[0][6]

    a[0] = []

    a[0].append(int(k))
    a[0].append(b)

    r.append(a)

print(r)