def save(model,filename):
    f = open(filename, 'w')
    for item in model:
        temp = list(model[item])
        temp.insert(0, item)
        temp.extend("\n")
        f.writelines(" ".join(str(s) for s in temp))
    f.close()