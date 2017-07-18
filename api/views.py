from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import math
import ast
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


def solvr(y, t, beta_h, theta_h, gama, beta_m, theta_m, f_e, f_l, f_p,
          mu_e, mu_l, mu_p, mu_m, pi, delta_l, sigma, b, eps, alpha, sprayTime, k, c, waterTime):

    #human init
    Sh = y[0]
    Eh = y[1]
    Ih = y[2]
    Rh = y[3]
    N = Sh + Eh + Ih + Rh

    #mosquito init
    Ev = y[4]
    Lv = y[5]
    Pv = y[6]
    Sm = y[7]
    Em = y[8]
    Im = y[9]
    M = Sm + Em + Im

    #human model
    dshdt = -  beta_h * Im * (1 - eps * b) * Sh
    dehdt = beta_h * Im * (1 - eps * b) * Sh - theta_h * Eh
    dihdt = theta_h * Eh - gama * Ih
    drhdt = gama * Ih

    #mosiquito model
    V=100
    if math.floor(t) in sprayTime:
        w_bar = 0.99 * (1 - np.exp(float(-V) / alpha * (Lv + Sm + Em + Im)))
    else:
        w_bar = 0

    if math.floor(t) in waterTime:
        k = k - c
    else:
        pass

    devdt = pi * (1 - float(Ev + Lv + Pv) / float(k * 125)) * \
        M - (f_e + mu_e) * Ev
    dlvdt = f_e * Ev - (f_l + mu_l + delta_l * Lv + w_bar) * Lv
    dpvdt = f_l * Lv - (f_p + mu_p) * Pv
    dsmdt = sigma * f_p * Pv - \
        (mu_m + w_bar + beta_m * Ih * (1 - eps * b)) * Sm
    demdt = beta_m * Ih * (1 - eps * b) * Sm - (theta_m + mu_m + w_bar) * Em
    dimdt = theta_m * Em - (mu_m + w_bar) * Im

    return [dshdt, dehdt, dihdt, drhdt, devdt, dlvdt, dpvdt, dsmdt, demdt, dimdt]




def seir(request):
    a_t = np.arange(215)
    # for key in request.GET:
    #     pa = key[4:].strip()
    #     if pa == "sprayTime" or pa == "waterTime":
    #         print(request.GET[key])
    #         locals()['{0}'.format(pa)] = ast.literal_eval(request.GET.getlist(key)[0])
    #     else :
    #         locals()['{0}'.format(pa)]= float(request.GET.getlist(key)[0])
    N = float(request.GET['paraN'])
    M = float(request.GET['paraM'])


    #human parameters
    beta_h = float(request.GET['parabeta_h'])
    theta_h = float(request.GET['paratheta_h'])
    gama = float(request.GET['paragama'])

    #mosquito paraneters
    beta_m = float(request.GET['parabeta_m'])
    theta_m = float(request.GET['paratheta_m'])
    f_e = float(request.GET['paraf_e'])
    f_l = float(request.GET['paraf_l'])
    f_p = float(request.GET['paraf_p'])
    mu_e = float(request.GET['paramu_e'])
    mu_l = float(request.GET['paramu_l'])
    mu_p = float(request.GET['paramu_p'])
    mu_m = float(request.GET['paramu_m'])
    pi = float(request.GET['parapi'])
    delta_l = float(request.GET['paradelta_l'])
    sigma = float(request.GET['parasigma'])

    #intervention parameters
    budget = float(request.GET['parabudget'])
    #1 bed net
    perNetCost = float(request.GET['paraperNetCost'])
    b = float(budget) / float(perNetCost) / float(N)
    eps = float(request.GET['paraeps'])
    #2 spray
    # the money of spray eaxh time?
    sprayTime = ast.literal_eval(request.GET['parasprayTime'])
    alpha = float(request.GET['paraalpha'])

    #3 removing water container
    # the money of removing each time
    waterTime = ast.literal_eval(request.GET['parawaterTime'])
    k = float(request.GET['parak'])
    c = float(request.GET['parac'])
    init = [N - 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]
    asol = integrate.odeint(solvr, init, a_t, args=(beta_h, theta_h, gama, beta_m,
                                                    theta_m, f_e, f_l, f_p, mu_e, mu_l, mu_p, mu_m, pi, delta_l, sigma, b, eps,
                                                    alpha, sprayTime, k, c, waterTime))
    asol = np.insert(asol, 0, a_t, axis=1)

    # asol = np.concatenate(([['date', 'S', 'E', 'I', 'R']], asol))
    mystr = json.dumps(asol, cls=MyEncoder, indent=4, separators=(',', ': '))
    return HttpResponse(mystr,  content_type='application/json')


