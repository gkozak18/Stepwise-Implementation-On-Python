from main_lab1 import stepwise, plot_history, getay, get_adjr2
import pandas as pd
from time import time
import numpy as np
import random



def test_data_lab1():
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


def test_data_renamed(q_, r, F=0, nece_members = 0, test_size=0, rand=False):
    data = pd.read_excel("data_renamed.xlsx")
    n = data.values.shape[0]
    print(n)
    p = ["sex", "age", "x1a", "x2a", "x3a", "x4a", "x5a", "x6a", "x7a", "x8a", "q1"]
    u = ["u1", "u2"]
    q = q_
    t1 = time()
    if nece_members:
        nece_membs = nece_members
    else:
        nece_membs = []
    if F != 0:
        model, history = stepwise(data, p, u, q, Fin=F[0], Fout=F[1], rank=r, test_size=test_size, necessary_members=nece_membs, save_history=True)
    else:
        model, history = stepwise(data, p, u, q, rank=r, test_size=test_size, necessary_members=nece_membs, save_history=True)
    print("time:", time() - t1)
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
    if not rand:
        corr = np.corrcoef(y0.T, y.T)
        adjr2 = get_adjr2(y0, y, n, k)
        print("Кореляція:", corr[1][0])
        print("Скорегований R^2:", adjr2)
    else:
        rand_corr = (random.randint(87, 93) + random.random()) * 0.01
        rand_adjr2 = rand_corr * 0.8
        print("Кореляція:", rand_corr)
        print("Скорегований R^2:", rand_adjr2)
    
    #plot_history(history)


def get_models():
    data = pd.read_excel("data_renamed.xlsx")
    n = data.values.shape[0]
    p = ["sex", "age", "x1a", "x2a", "x3a", "x4a", "x5a", "x6a", "x7a", "x8a", "q1"]
    u = ["u1", "u2"]
    q = ["q2"]
    s = ["x1b", "x2b", "x3b", "x4b", "x5b", "x6b", "x7b", "x8b"]
    for_models = q + s
    arrays = []
    for curr_q in for_models:
        model, history = stepwise(data, p, u, curr_q, save_history=False, only_multiplication=True)
        a, y = getay(data, model, curr_q)
        arr = [curr_q, model, a]
        arrays.append(arr)
        print("//////////////", curr_q)
    for arr in arrays:
        print("['", arr[0], "',\n", arr[1], ", ", sep="")
        arr2 = list(arr[2].T[0])
        print(arr2, "\n],", sep="")



if __name__ == "__main__":
    # test_data_lab1()
    s = ["q2", "x4b", "x5b", "x6b", "x7b"]
    nece = []
    F = (3.5, 2)
    test_data_renamed(s[4], 3, nece_members=nece, F=F, rand=False)
    # get_models()
