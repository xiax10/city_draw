'''use gradient descent to find the minimum value of a single variable function'''

from sympy import Derivative, Symbol, sympify
from sympy.plotting import plot
import math

def grad_descent(x0, f1x, x):
    epsilon = 1e-6
    step_size = 1e-1

    x_old = x0
    x_new = x_old - step_size * f1x.subs({x:x_old}).evalf()

    


    while abs(x_old - x_new) > epsilon:
        x_old = x_new
        x_new = x_old - step_size * f1x.subs({x:x_old}).evalf()
    

    return x_new

if __name__ == '__main__':
    f = input('Enter a function in one variable: ')
    var = input('Enter the variable to differentiate with respect to: ')
    var0 = float(input('Enter the initial value of the variable: '))

    try:
        f = sympify(f)
    except KeyError:
        print('invalid function entered')
    else:
        var = Symbol(var)
        
        p1 = plot(f, (var, -1,1), show=False)

        d = Derivative(f, var).doit()
        var_min = grad_descent(var0, d, var)

        p2 = plot(f,(var, var0, var_min), marker='.', show=False)
        print('{0}: {1}'.format(var.name, var_min))
        print('Minimum value: {0}'.format(f.subs({var:var_min})))

        p1.append(p2[0])
        p1.show()

