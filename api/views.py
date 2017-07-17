from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
from scipy import integrate
import json
# Create your views here.


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, str):
            return str(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.float):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

def solvr(y, t, mu, sigma, tau, delta, beta):

    S = y[0]
    E = y[1]
    I = y[2]
    R = y[3]
    N = S + E + I + R

    dsdt = mu * N - (beta * I + mu) * S
    dedt = beta * I * S - (sigma + mu) * E
    didt = sigma * E - (tau + mu + delta) * I
    drdt = tau * I - (mu) * R

    return [dsdt, dedt, didt, drdt]



def seir(request):
    a_t = np.arange(196)

    N = 1885542
    init = [N - 1, 0, 1, 0]

    mu = 1 / (3494 * 7)
    sigma = 1 / 7
    delta = (0.0035 / 7)
    tau = 1 / 7
    beta = 2.6389 / 7 / N
    asol = integrate.odeint(solvr, init, a_t, args=(mu, sigma, tau, delta, beta))    
    asol = np.insert(asol, 0, a_t, axis=1)

    # asol = np.concatenate(([['date', 'S', 'E', 'I', 'R']], asol))
    mystr = json.dumps(asol, cls=MyEncoder)
    return HttpResponse(mystr,  content_type='application/json')


