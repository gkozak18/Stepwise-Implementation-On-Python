import pandas as pd
import numpy as np


def getRSS(y, y0):
    res = sum((y0 - y)**2)
    return res


def getMSE(y, y0, k):
    RSS = getRSS(y, y0)
    n = len(y)
    res = RSS / (n - k - 2)
    return res


def getSSR(y, y0):
    mean0 = y0.mean()
    res = ((y - mean0)**2).sum()
    return res


def getdeltaSSR(y0, y1, y2):
    SSR1 = getSSR(y1, y0)
    SSR2 = getSSR(y2, y0)
    res = SSR2 - SSR1
    return res


def getF(y0, y1, y2, k):
    deltaSSR = getdeltaSSR(y0, y1, y2)
    MSE = getMSE(y2, y0, k)
    res = deltaSSR / MSE
    return res, deltaSSR, MSE


def getcandidates(p, u):
    res = p + u
    for i in p:
        for j in p:
            res.append(i+"*"+j)
            res.append(i+"/"+j)
            for k in u:
                res.append(i+"*"+j+"/"+k)
                res.append(i+"/"+j+"*"+k)
    for i in p:
        for j in p:
            for k in p:
                for d in u:
                    pass
                    #res.append(i+"*"+j+"/"+k+"*"+d)
                    #res.append(i+"/"+j+"*"+k+"/"+d)
                    
    return res


def printxy(x, y):
    for i in zip(x, y):
        print(i[0], i[1])


def getay(data, model, q):
    x = []
    y = np.array([data[q].to_numpy()]).T
    for col in data.columns:
        exec(col + " = data['" + col + "'].to_numpy()")
    for i in model:
        x.append(eval(i))
    x.append(np.ones(data[q].shape[0]))
    x = np.array(x).T
    #printxy(x, y)
    x1 = x.T @ x
    #print(x1)
    try:
        x2 = np.linalg.inv(x1)
    except:
        #print(x1)
        return [0], 0
    #print(x2)
    x3 = x2 @ x.T
    #print(x3)
    a = x3 @ y
    #print(a)
    y1 = x @ a
    #print(y1)
    return a, y1


def checknew(data, model, new, q, Finc):
    a1, y1 = getay(data, model, q)
    a2, y2 = getay(data, model + [new], q)
    if a1[0] == 0 or a2[0] == 0:
        print("singmat", new)
        return False
    y = np.array([data[q].to_numpy()]).T
    F = getF(y, y1, y2, a2.shape[0])
    if new == "x4a/x3a*x3a/u1":
        print("a1", a1)
        print("y1", y1)
        print("a2", a2)
        print("y2", y2)
        print("deltaSSR", F[1], "MSE", F[2])
        print("F", F[0], new)
        return False
    print("F", F[0], new)
    return F[0][0] > Finc


def checkold(data, model, old, q, Fout):
    old_model = model + []
    old_model.remove(old)
    a1, y1 = getay(data, old_model, q)
    a2, y2 = getay(data, model, q)
    y = np.array([data[q].to_numpy()]).T
    F = getF(y, y1, y2, a2.shape[0])
    #print("F", F, old)
    return F[0] < Fout


def stepwise(data, p, u, q):
    candidates = getcandidates(p, u)
    members = []
    for candidate in candidates:
        if checknew(data, members, candidate, q, 3.87):
            members.append(candidate)
            print(candidate, "was added")
            for memb in members:
                if checkold(data, members, memb, q, 2.71):
                    members.remove(memb)
                    print(memb, "was removed")
    return members


if __name__ == "__main__":
    data = pd.read_excel("data_renamed.xlsx")
    p = ["x1a", "x2a", "x3a", "x4a", "x5a", "x6a", "x7a", "x8a", "q1"]
    u = ["u1", "u2"]
    q = "q2"
    model = stepwise(data, p, u, q)
    print("Model:", model)
    y0 = np.array([data[q].to_numpy()]).T
    a, y = getay(data, model, q)
    print("A:", a)
    corr = np.corrcoef(y0.T, y.T)
    print("corr:", corr)

