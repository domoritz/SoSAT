# SoSAT

[![Build Status](https://travis-ci.org/domoritz/SoSAT.png)](https://travis-ci.org/domoritz/SoSAT)

A SAT solver that uses different statistical optimization algorithms to solve SAT problems encoded in the [DIMACS format](http://www.satcompetition.org/2009/format-benchmarks2009.html). This solver is written in Python and uses Numpy to speed up calculations. The three main algorithms in this solver are a *ant colony optimization algorithm*, a *genetic algorithm*, and *walkSAT*. To support these algorithms, there are some preprocessing algorithms.


## Features

* 3 optimization algorithms
  * ant colony optimization algorithm
  * genetic algorithm
  * walkSAT
* factorization, reduction and simulated annealing for preprocessing
* parallel evaluation from different starting points
* configurable profiles to parameterize the solver


## Installation

**Create a virtual environment**

```bash
virtualenv venv
```

**Activate the virtual env**

```bash
source venv/bin/activate
```

**Install the solver**

```bash
python setup.py install
```

**Run it**

```bash
sosat --help
```