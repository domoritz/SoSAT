# SoSAT

[![Build Status](https://travis-ci.org/domoritz/SoSAT.png)](https://travis-ci.org/domoritz/SoSAT)

A SAT solver that uses different statistical optimization algorithms to solve SAT problems encoded in the DIMACS format. This solver is written in Python and uses Numpy to speed up calculations. The two main algorithms in this solver are a *ant colony optimization algorithm* and a *genetic algorithm*. To support these algorithms, there are some preprocessing algorithms.

# Installation

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