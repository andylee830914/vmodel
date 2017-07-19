from django.shortcuts import render

# Create your views here.


def model(request):
    
    parameter = {
        # human parameters
        'N'             : {'name': r'N'             ,'show': 1 , 'default': 526007},
        'beta_h'        : {'name': r'\(\beta_h\)'   ,'show': 1 , 'default': 0.75},
        'theta_h'       : {'name': r'\(\theta_h\)'  ,'show': 0 , 'default': 0.1},
        'gama'          : {'name': r'\(\gamma\)'    ,'show': 0 , 'default': 0.143},

        # mosquito paraneters
        'beta_m'        : {'name': r'\(\beta _m\)'  ,'show': 1 , 'default': 0.375},
        'theta_m'       : {'name': r'\(\theta _m\)' ,'show': 0 , 'default': 0.2},
        'f_e'           : {'name': r'\(f_e\)'       ,'show': 0 , 'default': 0.276},
        'f_l'           : {'name': r'\(f_l\)'       ,'show': 0 , 'default': 0.11},
        'f_p'           : {'name': r'\(f_p\)'       ,'show': 0 , 'default': 0.253},
        'mu_e'          : {'name': r'\(\mu_e\)'     ,'show': 0 , 'default': 0.05},
        'mu_l'          : {'name': r'\(\mu_l\)'     ,'show': 0 , 'default': 0.05},
        'mu_p'          : {'name': r'\(\mu_p\)'     ,'show': 0 , 'default': 0.0167},
        'mu_m'          : {'name': r'\(\mu_m\)'     ,'show': 0 , 'default': 0.047},
        'pi'            : {'name': r'\(\pi\)'       ,'show': 0 , 'default': 1},
        'r'             : {'name': r'r'             ,'show': 0 , 'default': 13.6},
        'sigma'         : {'name': r'\(\sigma\)'    ,'show': 0 , 'default': 0.5},

        # intervention parameters
        'budget'        : {'name': r'budget'        ,'show': 1, 'default': 0},
        'perWorkCost'   : {'name': r'perWorkCost'   ,'show': 1, 'default': 1064},
        
        # 1 bed net
        'perNetCost'    : {'name': r'perNetCost'    ,'show': 1 , 'default': 0},
        'eps'           : {'name': r'\(\epsilon\)'  ,'show': 0 , 'default': 0.67},
        # 2 spray
        # the money of spray eaxh time?
        # [50,100,150,200]
        'perPestCost'   : {'name': r'perPestCost'   ,'show': 1 , 'default': 0.38},
        'perWorkLength' : {'name': r'perWorkLength' ,'show': 1 , 'default': 1*1000*8},        
        'sprayTime'     : {'name': r'sprayTime'     ,'show': 1 , 'default': []},
        'area'          : {'name': r'area'          ,'show': 0 , 'default': 5.709296*1000000},
        'roadLength'    : {'name': r'roadLength'    ,'show': 0 , 'default': 527.927*1000},

        # 3 removing water container
        # the money of removing each time
        'waterTime'     : {'name': r'waterTime'      ,'show': 1 , 'default': []},  # [50,100,150,200]
        'k'             : {'name': r'k'              ,'show': 0 , 'default': 89742},
    }
    pasort = sorted(parameter.items(), key=lambda x: x[1]['show'], reverse=True)

    return render(request, 'chart.html', {'parameter': parameter, 'pasort': pasort})
