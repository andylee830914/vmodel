from django.shortcuts import render

# Create your views here.


def model(request):
    result = {
        'Sh': {'name': r'\(S_h\)', 'show':1},
        'Eh': {'name': r'\(E_h\)', 'show':2},
        'Ih': {'name': r'\(I_h\)', 'show':3},
        'Rh': {'name': r'\(R_h\)', 'show':4},
        'Ev': {'name': r'\(E_v\)', 'show':5},
        'Lv': {'name': r'\(L_v\)', 'show':6},
        'Pv': {'name': r'\(P_v\)', 'show':7},
        'Sm': {'name': r'\(S_m\)', 'show':8},
        'Em': {'name': r'\(E_m\)', 'show':9},
        'Im': {'name': r'\(I_m\)', 'show':10}
    }

    parameter = {
        'day'           : {'name': r'Day'           ,'show': 11 , 'default': 200},

        # human parameters
        'N'             : {'name': r'N'             ,'show': 10 , 'default': 526007},
        'beta_h'        : {'name': r'\(\beta_h\)'   ,'show': 9 , 'default': 0.375},
        'theta_h'       : {'name': r'\(\theta_h\)'  ,'show': 0 , 'default': 0.1},
        'gama'          : {'name': r'\(\gamma\)'    ,'show': 0 , 'default': 0.143},

        # mosquito paraneters
        'beta_m'        : {'name': r'\(\beta _m\)'  ,'show': 8 , 'default': 0.75},
        'theta_m'       : {'name': r'\(\theta _m\)' ,'show': 0 , 'default': 0.2},
        'f_e'           : {'name': r'\(f_e\)'       ,'show': 0 , 'default': 0.276},
        'f_l'           : {'name': r'\(f_l\)'       ,'show': 0 , 'default': 0.11},
        'f_p'           : {'name': r'\(f_p\)'       ,'show': 0 , 'default': 0.253},
        'mu_e'          : {'name': r'\(\mu_e\)'     ,'show': 0 , 'default': 0.05},
        'mu_l'          : {'name': r'\(\mu_l\)'     ,'show': 0 , 'default': 0.05},
        'mu_p'          : {'name': r'\(\mu_p\)'     ,'show': 0 , 'default': 0.0167},
        'mu_m'          : {'name': r'\(\mu_m\)'     ,'show': 0 , 'default': 0.047},
        'pi'            : {'name': r'\(\pi\)'       ,'show': 0 , 'default': 1},
        'r'             : {'name': r'r'             ,'show': 0 , 'default': 100},
        'sigma'         : {'name': r'\(\sigma\)'    ,'show': 0 , 'default': 0.5},

        # intervention parameters
        'budget'        : {'name': r'budget'        ,'show': 7, 'default': 0},
        'perWorkCost'   : {'name': r'perWorkCost'   ,'show': 6, 'default': 1064},
        
        # 1 bed net
        'perNetCost'    : {'name': r'perNetCost'    ,'show': 5 , 'default': 90},
        'eps'           : {'name': r'\(\epsilon\)'  ,'show': 0 , 'default': 0.67},
        # 2 spray
        # the money of spray eaxh time?
        # [50,100,150,200]
        'perPestCost'   : {'name': r'perPestCost'   ,'show': 4 , 'default': 0.38},
        'perWorkLength' : {'name': r'perWorkLength' ,'show': 3 , 'default': 1*1000*8},        
        'sprayTime'     : {'name': r'sprayTime'     ,'show': 2, 'default': []},
        'area'          : {'name': r'area'          ,'show': 0 , 'default': 5.709296*1000000},
        'roadLength'    : {'name': r'roadLength'    ,'show': 0 , 'default': 527.927*1000},

        # 3 removing water container
        # the money of removing each time
        'waterTime'     : {'name': r'waterTime'      ,'show': 1, 'default': []},  # [50,100,150,200]
        'k'             : {'name': r'k'              ,'show': 0 , 'default': 89742},
    }
    pasort = sorted(parameter.items(), key=lambda x: -1*x[1]['show'])
    resort = sorted(result.items(), key=lambda x: x[1]['show'])

    
    return render(request, 'chart.html', {'parameter': parameter, 'pasort': pasort, 'result': result, 'resort': resort })
