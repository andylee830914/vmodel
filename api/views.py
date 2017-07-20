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
          mu_e, mu_l, mu_p, mu_m, pi, r, sigma, b, eps, w, sprayTime, c,
          waterTime):

    #human init
#human init
    Sh = y[0]
    Eh = y[1]
    Ih = y[2]
    Rh = y[3]
    N  =  Sh + Eh + Ih + Rh

    #mosquito init
    Ev = y[4]
    Lv = y[5]
    Pv = y[6]
    Sm = y[7]
    Em = y[8]
    Im = y[9]
    M = Sm + Em + Im

    #environmental init
    K = y[10]

    #human model
    dshdt =                                               -  float(beta_h * Im * (1-eps*b))/float(N)  * Sh
    dehdt = float(beta_h * Im * (1-eps*b))/float(N) * Sh  -  theta_h                                  * Eh
    dihdt = theta_h                 * Eh                  -  gama                                     * Ih
    drhdt = gama                    * Ih

    #mosiquito model
    if math.floor(t) in sprayTime:
        w_l = (1-f_l-mu_l*(1+r*float(Ev+Lv+Pv)/float(K)))*w
        w_Sm = (1-float(beta_m*Ih * (1-eps*b))/float(M)-mu_m)*w
        w_Em = (1-theta_m-mu_m)*w
        w_Im = (1-mu_m)*w
    else:
        w_l = 0
        w_Sm = 0
        w_Em = 0
        w_Im = 0


    if math.floor(t) in waterTime:
        k = c
        if k > 1: k = 1

        k_e = (1-f_e-mu_e)*k
        k_l = (1-f_l-mu_l*(1+r*float(Ev+Lv)/float(K)))*k
        k_p = (1-f_p-mu_p)*k

        dkdt = -k*K
    else:
        k_e = 0
        k_l = 0
        k_p = 0
        dkdt = 0

    lay = 1-float(Ev+Lv+Pv)/float(K*50)
    if lay < 0:
        lay = 0

    devdt = pi * lay                              * M   -  (f_e + mu_e*(1+r*float(Ev+Lv+Pv)/float(K)) + k_e)         * Ev
    dlvdt = f_e                                   * Ev  -  (f_l + mu_l*(1+r*float(Ev+Lv+Pv)/float(K)) + w_l + k_l)   * Lv
    dpvdt = f_l                                   * Lv  -  (f_p + mu_p*(1+r*float(Ev+Lv+Pv)/float(K)) + k_p)         * Pv
    dsmdt = sigma * f_p                           * Pv  -  (mu_m + w_Sm + float(beta_m*Ih * (1-eps*b))/float(M))     * Sm
    demdt = float(beta_m*Ih * (1-eps*b))/float(M) * Sm  -  (theta_m + mu_m + w_Em)                                   * Em
    dimdt = theta_m                               * Em  -  (mu_m + w_Im)                                             * Im


    return [dshdt,dehdt,dihdt,drhdt,devdt,dlvdt,dpvdt,dsmdt,demdt,dimdt,dkdt]




def model(request):
    day = int(request.GET['paraday'])
    a_t = np.arange(day)
    # for key in request.GET:
    #     pa = key[4:].strip()
    #     if pa == "sprayTime" or pa == "waterTime":
    #         print(request.GET[key])
    #         locals()['{0}'.format(pa)] = ast.literal_eval(request.GET.getlist(key)[0])
    #     else :
    #         locals()['{0}'.format(pa)]= float(request.GET.getlist(key)[0])
    N = float(request.GET['paraN'])


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
    r = float(request.GET['parar'])
    sigma = float(request.GET['parasigma'])

    #intervention parameters
    budget = float(request.GET['parabudget'])
    perWorkCost = float(request.GET['paraperWorkCost'])  # basic (unit:NT$)

    #1 bed net
    perNetCost = float(request.GET['paraperNetCost'])

    if float(perNetCost)==0 :
        b=0
    else:
        b = float(budget) / float(perNetCost) / float(N)

    eps = float(request.GET['paraeps'])
    #2 spray
    # the money of spray eaxh time?
    # bascic (unit: NT$/ml)
    perPestCost = float(request.GET['paraperPestCost'])
    # advanced (unit:meter)
    perWorkLength = float(request.GET['paraperWorkLength'])
    sprayTime = ast.literal_eval(request.GET['parasprayTime'])  # advanced
    area = float(request.GET['paraarea'])  # advanced (unit: m-square)
    roadLength = float(request.GET['pararoadLength'])  # advanced (unit: meter)
    if len(sprayTime)!=0:
        perTimeBudget1 = float(budget)/float(len(sprayTime))
        roadDensity = float(roadLength) / float(area)
        sprayArea = float(perTimeBudget1)/float(0.04*perPestCost+float(roadDensity)/float(perWorkLength)*perWorkCost)
        w = float(sprayArea)/float(area)
        if w > 1: w = 1
    else:
        w=0

    #3 removing water container
    # the money of removing each time
    k = float(request.GET['parak'])
    waterTime = ast.literal_eval(request.GET['parawaterTime'])
    if len(waterTime) != 0:
        perTimeBudget2 = float(budget) / float(len(waterTime))
        c = float(perTimeBudget2) / \
            ((float(roadLength) / 171710 * 298) * float(perWorkCost))
    else :
        c = 0
    
    init = [N - 20001, 0, 1, 20000, 30000, 110000, 50000, 40000, 0, 0, 89742]
    asol = integrate.odeint(solvr, init, a_t, args=(beta_h, theta_h, gama, beta_m,
                                                    theta_m, f_e, f_l, f_p, mu_e, mu_l, mu_p, mu_m, pi, r, sigma, b, eps,
                                                    w, sprayTime, c, waterTime))
    asol = np.insert(asol, 0, a_t, axis=1)

    # asol = np.concatenate(([['date', 'S', 'E', 'I', 'R']], asol))
    mystr = json.dumps(asol, cls=MyEncoder, indent=4, separators=(',', ': '))
    return HttpResponse(mystr,  content_type='application/json')


