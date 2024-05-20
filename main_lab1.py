import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from time import time


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
    best = ((y0 - mean0)**2).sum()
    if res > best:
        print("WTF SSR is higher then possible")
        print("possible:", best)
        print("current:", res)
        return 0
    return res


def getdeltaSSR(y0, y1, y2):
    SSR1 = getSSR(y1, y0)
    SSR2 = getSSR(y2, y0)
    res = SSR2 - SSR1
    return res


def get_adjr2(y, y_pred, n, k):
    r2 = r2_score(y, y_pred)
    adjr2 = 1 - ((1 - r2) * (n - 1)/(n - k - 1))
    return adjr2


def getF(y0, y1, y2, k):
    deltaSSR = getdeltaSSR(y0, y1, y2)
    MSE = getMSE(y2, y0, k)
    res = deltaSSR / MSE
    return res, deltaSSR, MSE


def getcandidates(p, u, rank=2):
    res = p + u
    for i in p:
        for j in p:
            res.append(i+"*"+j)
            if i != j:
                res.append(i+"/"+j)
            for k in u:
                res.append(i+"*"+j+"/"+k)
                if i != j:
                    res.append(i+"/"+j+"*"+k)
    if rank == 3:
        for i in p:
            for j in p:
                for k in p:
                    if j != k and i != k:
                        res.append(i+"*"+j+"/"+k)
                    if i != j and i != k:
                        res.append(i+"/"+j+"*"+k)
                    for d in u:
                        if j != k and i != k:
                            res.append(i+"*"+j+"/"+k+"*"+d)
                            res.append(i+"*"+j+"/"+k+"/"+d)
                        if i != j and i != k:
                            res.append(i+"/"+j+"*"+k+"*"+d)
                            res.append(i+"/"+j+"*"+k+"/"+d)          
    return res


def printxy(x, y):
    for i in zip(x, y):
        print(i[0], i[1])


def getay(data, model, q):
    x = []
    y0 = np.array([data[q].to_numpy()]).T
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
    try:
        a = x3 @ y0
    except:
        print(x3, y0)
    #print(a)
    y1 = x @ a
    #print(y1)
    return a, y1


def checknew(data, model, new, q, Finc, printF=False):
    a1, y1 = getay(data, model, q)
    a2, y2 = getay(data, model + [new], q)
    if a1[0] == 0 or a2[0] == 0:
        print("singmat", new)
        return False
    y = np.array([data[q].to_numpy()]).T
    F = getF(y, y1, y2, a2.shape[0])
    if new == "fuck":
        print("a1", a1)
        print("y1", y1)
        print("a2", a2)
        print("y2", y2)
        print("deltaSSR", F[1], "MSE", F[2])
        print("F", F[0], new)
        return False
    #print("deltaSSR", F[1], "MSE", F[2])
    if printF:
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


def stepwise(data, p, u, q, test_size=0.2, save_history=True, print_addings=False, rank=2):
    train_data, test_data = train_test_split(data, test_size=test_size, random_state=42)
    candidates = getcandidates(p, u, rank=rank)
    members = []

    n = train_data.values.shape[0]
    train_y0 = np.array([train_data[q].to_numpy()]).T
    test_y0 = np.array([test_data[q].to_numpy()]).T
    adding_history = []
    train_corr_history = []
    train_adjr2_history = []
    test_corr_history = []
    test_adjr2_history = []
    for candidate in candidates:
        if checknew(train_data, members, candidate, q, 3.87):
            members.append(candidate)
            if print_addings:
                print(candidate, "was added")
            
            # history stuff
            if save_history:
                adding_history.append("+" + candidate)
                train_a, train_y = getay(train_data, members, q)
                test_a, test_y = getay(test_data, members, q)
                k = len(members)
                train_corr_history.append(np.corrcoef(train_y0.T, train_y.T)[1][0])
                train_adjr2_history.append(get_adjr2(train_y0, train_y, n, k))
                test_corr_history.append(np.corrcoef(test_y0.T, test_y.T)[1][0])
                test_adjr2_history.append(get_adjr2(test_y0, test_y, n, k))
            
            for memb in members:
                if checkold(train_data, members, memb, q, 2.71):
                    members.remove(memb)
                    if print_addings:
                        print(memb, "was removed")

                    # history stuff
                    if save_history:
                        adding_history.append("-" + memb)
                        train_a, train_y = getay(train_data, members, q)
                        test_a, test_y = getay(test_data, members, q)
                        k = len(members)
                        train_corr_history.append(np.corrcoef(train_y0.T, train_y.T)[1][0])
                        train_adjr2_history.append(get_adjr2(train_y0, train_y, n, k))
                        test_corr_history.append(np.corrcoef(test_y0.T, test_y.T)[1][0])
                        test_adjr2_history.append(get_adjr2(test_y0, test_y, n, k))

    history = {"adding": adding_history,
               "train_corr": train_corr_history,
               "train_adjr2": train_adjr2_history,
               "test_corr": test_corr_history,
               "test_adjr2": test_adjr2_history}
    
    return members, history


def plot_history(history):
    x = history["adding"]
    y1 = history["train_corr"]
    y2 = history["train_adjr2"]
    y3 = history["test_corr"]
    y4 = history["test_adjr2"]

    plt.figure(figsize=(10, 5))

    plt.plot(x, y1, label="train_corr")
    plt.plot(x, y2, label="train_adjr2")
    plt.plot(x, y3, label="test_corr")
    plt.plot(x, y4, label="test_adjr2")

    plt.title("Історія кореліції та зваженної детермінації при роботі stepwise")
    plt.xlabel("Додавання та видалення різних змінних моделі")
    plt.ylabel("Зміна показників")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=60)
    plt.subplots_adjust(bottom=0.2)

    plt.show()


if __name__ == "__main__":
    data = pd.read_excel("data_lab1a.xlsx")
    n = data.values.shape[0]
    print(n)
    p = ["S", "d1", "d2", "d3", "P6", "P1", "pdsp", "pdsn", "L", "W", "WI",
         "Ff", "Mm", "Wo", "Kk", "Bk", "Bp", "El", "H", "DMr", "DMl", "DMm",
         "Mc", "Dc", "GZ", "PSH", "PG", "Bs", "IK", "U", "Pp", "Po1",
         "Po2", "F"]
    u = []
    q = "VB"
    t1 = time()
    model, history = stepwise(data, p, u, q, save_history=True)
    print("time:", time() - t1)
    #print("Model:", model)
    y0 = np.array([data[q].to_numpy()]).T
    k = len(model)
    a, y = getay(data, model, q)
    #print("A:", a)
    print("Результати:")
    print("Кількість змінних що увійшли у модель(без врахування вільного члену):", len(model))
    print("Зміні котрі увійшли у модель та коефіцієнти перед ними:")
    for i in zip(model, a):
        print(i[0], ": ", i[1][0], sep="")
    print("Вільний член:", a[-1][0])
    corr = np.corrcoef(y0.T, y.T)
    print("Кореляція:", corr[1][0])
    adjr2 = get_adjr2(y0, y, n, k)
    print("Скорегований R^2:", adjr2)

    plot_history(history)

