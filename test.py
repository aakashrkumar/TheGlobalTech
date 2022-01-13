s = 0
# 2, 1, 3, 2, 5, 4, 6, 5
series = []
for i in range(0, 100000):
    if i % 2 == 0:
        s += 2
    else:
        s -= 1

    series.append(s)
print(series)
i = 10000
print(series[i - 1] / i)
