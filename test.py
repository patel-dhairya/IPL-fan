
def func(t_overs):
    return int(float(t_overs)) * 6 + round(10 * (t_overs - int(t_overs)))


overs = [3, 3.1, 3.2, 3.3, 3.4, 3.5, 4]

for over in overs:
    print(func(over))
