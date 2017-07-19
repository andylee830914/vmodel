# vmodel

### Feature
- Visualization of Epidemic Model Simulation
- Solve model in different parameters
- Date Range Filter


### Structure
This project based on Django Web Framework and Google Chart API. 

- API (Backend) :
Solve epidemic model with `scipy` and return the result in JSON.
- Visual (Frontend) :
Call the API and draw the line chart with Google Chart.

### Simulate with your model
- Modified your model in `solvr` function which in `api/views.py`
- Make sure all of your parameters in `model` function which in `api/views.py` set as below ```N=float(request.GET['paraN'])```
- Make sure your Solver (for example, in this project we use `odeint` which in  `scipy`) is set
- List all of your parameter dictionary in `model` function which in `visual/views.py` with `name,show,default`
  * name : Parameter name which show on Web 
  * show : You can determine parameters are basic or adavance
  * default : Default value of the parameter

### Getting Started
```
python manage.py runserver
```

then view the web at http://127.0.0.1:8000/visual/
