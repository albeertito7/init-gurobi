import gurobipy as gp
from gurobipy import GRB

# Resource and job sets
R = ['Carlos', 'Joe', 'Monika']
J = ['Tester', 'JavaDeveloper', 'Architect']

# Matching score data
combinations, scores = gp.multidict({
    ('Carlos', 'Tester'): 53,
    ('Carlos', 'JavaDeveloper'): 27,
    ('Carlos', 'Architect'): 13,
    ('Joe', 'Tester'): 80,
    ('Joe', 'JavaDeveloper'): 47,
    ('Joe', 'Architect'): 67,
    ('Monika', 'Tester'): 53,
    ('Monika', 'JavaDeveloper'): 73,
    ('Monika', 'Architect'): 47
})

# Declare and initialize model
m = gp.Model('RAP')

# Create decision variables for the RAP model
x = m.addVars(combinations, name="assign")

"""
# other way to add the vars manually and not using addVars like before
x = {}
for c in combinations:
    x[c] = m.addVar(name="assign[%s, %s]", vtype=GRB.CONTINUOUS, lb=4, ub=10) # by deault CONTINUOUS, other types GRB.BINARY, GRB.INTEGER


m.update()
for key in x:
        print(key, x[key], x[key].Vtype, x[key].lb, x[key].ub)

# lowerbound = lb
# upperbound = ub
## interval, to reduce the problem space
"""
"""
for job in J:
    exp = 0 # an expression, will become our constraint (a linear combination)
    for res in R:
        #print((res, job))
        exp += x[(res, job)] #summing the columns
    print("Sum == 1")
    m.addConstr(exp == 1)
"""

# Create job constraints
jobs = m.addConstrs((x.sum('*',j) == 1 for j in J), name='job')

"""
for res in R:
    exp = 0 # an expression, will become our constraint (a linear combination)
    for job in J:
        #print("x[", (res, job),"]")
        exp += x[(res, job)] #summing the columns
    print("Sum == 1")
    m.addConstr(exp == 1)
"""

# Create resource constraints
resources = m.addConstrs((x.sum(r,'*') <= 1 for r in R), name='resource')