from django.shortcuts import render

# Create your views here.


def seir(request):

    parameter = {'N': 1885542, 'beta': 2.6389 / 7 / 1885542, 'mu': 1 /
                 (3494 * 7), 'sigma': 1 / 7, 'delta': 0.0035 / 7, 'tau': 1 / 7}

    return render(request, 'chart.html', {'parameter': parameter})
