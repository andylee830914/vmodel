from django.shortcuts import render

# Create your views here.


def seir(request):

    parameter = {'N': 1885542, 'beta': 2.6389 / 7 / 1885542, 'mu': 1 /
                 (3494 * 7), 'sigma': 1 / 7, 'delta': 0.0035 / 7, 'tau': 1 / 7}

    


    #human parameters
    parameter = {
        'N' : 500000,
        'M' : 0,
        'beta_h': 0.75,
        'theta_h': 0.1,
        'gama': 0.143,

        #mosquito paraneters
        'beta_m': 0.375,
        'theta_m': 0.2,
        'f_e': 0.276,
        'f_l': 0.11,
        'f_p': 0.253,
        'mu_e': 0.05,
        'mu_l': 0.05,
        'mu_p': 0.0167,
        'mu_m': 0.047,
        'pi': 1,
        'delta_l': 0.01,
        'sigma': 0.5,

        #intervention parameters
        'budget': 1000000,
        #1 bed net
        'perNetCost': 400,
        'eps': 0.67,
        #2 spray
        # the money of spray eaxh time?
        'sprayTime': [50, 100, 150, 200],  # [50,100,150,200]
        'alpha': 1 / 75000,

        #3 removing water container
        # the money of removing each time
        'waterTime': [],  # [50,100,150,200]
        'k': 1000,
        'c': 0
    }

    return render(request, 'chart.html', {'parameter': parameter})
