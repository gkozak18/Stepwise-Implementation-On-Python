import sympy as sp


models = [
    ['q2',
    ['q1', 'u2', 'x3a/x5a', 'x6a/x7a*u1'],
    [0.9122584018511952, -0.0016865078238164875, 0.4796745311449333, -0.00048011956946664944, -0.051678482490271106]
    ],
    ['x1b',
    ['x1a', 'sex/x8a'],
    [0.6701533368300735, 70.03354681121276, -0.46748860758590893]
    ],
    ['x2b',
    ['x2a', 'x5a', 'sex*x2a/u1'],
    [0.5578933202290607, -0.29964490929857274, -16.234765139707974, 16.07281175566726]
    ],
    ['x3b',
    ['x5a*x6a/u1', 'x7a*x1a/u2'],
    [-0.2391081018540299, -49.92784236428645, 54.49111447063147]
    ],
    ['x4b',
    ['age/x7a', 'x3a/x2a*u1'],
    [-4.124157079526016, 0.052652299443743764, 44.72496617203515]
    ],
    ['x5b',
    ['sex/age*u2', 'sex/x1a', 'age/x4a', 'x4a/x6a'],
    [0.8767080413191147, -5.98927387791445, 2.3840836893449993, 12.49843264171742, 2.1124430224716724]
    ],
    ['x6b',
    ['age*x1a/u2', 'age*x3a', 'age/x6a*u2'],
    [4.316067125557627, 0.002885680688749453, -0.08068400423899823, 116.82824991351865]
    ],
    ['x7b',
    ['x7a', 'x8a', 'age*x2a/u2', 'age*x3a', 'age*x4a', 'x3a/x4a'],
    [0.5951748893312372, -0.0020301912604489903, 0.05257406504530359, 0.0018283948348046006, -0.002494222742534147, -3.300866211679713, 7.552659769544934]
    ],
    ['x8b',
    ['x8a', 'x6a*x8a/u1', 'x8a/x6a*u1'],
    [5.091566518324216, -2.2317241182815915, -2.4153445948234564, 132.6777335286639]
    ]
]


def make_functions(vars, values):
    res = ""
    for i, var in enumerate(vars):
        res += str(values[i]) + "*" + var + "+"
    res += str(values[-1])
    return res


def replace_with_values(models, values):
    arrays = []
    for model in models:
        function = make_functions(model[1], model[2])
        function_expr = sp.sympify(function)
        symbols_dict = {var: sp.symbols(var) for var in values[0]}
        result = function_expr.subs({symbols_dict[var]: value for var, value in zip(values[0], values[1])})
        arr = [model[0], result]
        arrays.append(arr)
    return arrays

