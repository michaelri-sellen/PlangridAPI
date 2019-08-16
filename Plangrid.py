import Demo1, Demo2

switcher = {
    1: Demo1,
    2: Demo2
}

print("Which demo would you like to run")
print(list(switcher.keys()))
demonum = input()

switcher.get(int(demonum)).RunDemo()