# -*- coding: utf-8 -*-
"""AI-Lab-Exam-Problem-2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u8JKBJ6VxSweMJpC3O43RY7bPBUmCfLO
"""

pip install pulp

import pulp

# Define the decision variables
T = 52 # number of weeks
x = pulp.LpVariable.dicts('x', range(T), lowBound=0, cat='Integer')
b_normal = pulp.LpVariable.dicts('b_normal', range(T+1), lowBound=0, cat='Integer')
b_covid = pulp.LpVariable.dicts('b_covid', range(T+1), lowBound=0, cat='Integer')

# Define the problem
prob = pulp.LpProblem('Hospital Management', pulp.LpMinimize)

# Define the objective function
CP = 0.1 # example covid positivity rate
obj = pulp.lpSum([1000 * CP * (0.005 * b_normal[t] + 0.01 * b_covid[t] + 0.02 * x[t]) + 100000 * (0.0117 * CP * 0.02 * x[t]) for t in range(T)])
prob += obj

# Add constraints
b_normal[0] = 650 # initial number of normal beds
for t in range(T):
    prob += x[t] <= b_normal[t] # conversion cannot exceed available normal beds
    prob += x[t] + b_covid[t] <= b_normal[t] + b_normal[0] # total covid beds cannot exceed total available beds
    b_normal[t+1] = b_normal[t] - x[t] + b_covid[t] # update normal beds for next week
    b_covid[t+1] = b_covid[t] + x[t] # update covid beds for next week