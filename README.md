# Modelling and Simulation Project: A Genetic Algorithm Bridge Builder

## Running the simulation

### Requirements:
This project has been tested to work on:
```
Python version 3.10.12
pip 22.0.2
```

### Installing dependencies:
```
python3 -m venv ./venv
```
```
source ./venv/bin/activate{.shell}
```
```
pip install -r requirements.txt
```

### Running the project
```
python src/main.py genetic
```
This command allows you to run the genetic search algorithm.
```
python src/main.py gene GENE_STRING
```
This commands opens a graphical version of the simulation. SPACE starts and pauses the simulation and R restarts it.
```
python src/main.py interactive
```
This command allows you to build a bridge using your mouse. Note that this does not give you a string representation of the bridge.
