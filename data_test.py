from main_lab1 import stepwise, plot_history, getay, get_adjr2
import pandas as pd
from time import time
import numpy as np



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


def test_data_renamed():
    data = pd.read_excel("data_renamed.xlsx")
    n = data.values.shape[0]
    print(n)
    p = ["sex", "age", "x1a", "x2a", "x3a", "x4a", "x5a", "x6a", "x7a", "x8a", "q1"]
    u = ["u1", "u2"]
    q = "q2"
    t1 = time()
    model, history = stepwise(data, p, u, q, save_history=True)
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
    corr = np.corrcoef(y0.T, y.T)
    print("Кореляція:", corr[1][0])
    adjr2 = get_adjr2(y0, y, n, k)
    print("Скорегований R^2:", adjr2)

    plot_history(history)


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
        model, history = stepwise(data, p, u, curr_q, save_history=False)
        a, y = getay(data, model, curr_q)
        arr = [curr_q, model, a]
        arrays.append(arr)
        print("//////////////", curr_q)
    for arr in arrays:
        print("['", arr[0], "',\n", arr[1], ", ", sep="")
        arr2 = list(arr[2].T[0])
        print(arr2, "\n],", sep="")



if __name__ == "__main__":
    test_data_lab1()
    # test_data_renamed()
    # get_models()
