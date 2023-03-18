def files():
    t = input("Enter the word\n")
    f = open("search_results.txt")
    x = f.readlines()
    for i in range(0, len(x)):
        w = x[i]
        n = w.replace("\n", "")

        f1 = open(str(n))
        b = f1.readlines()
        for y in b:
            if t in y:
                f2 = open("sample.txt", "a")
                f2.write(str(y))
files()
