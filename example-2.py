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
x = {}
for c in combinations:
    x[c] = m.addVar(name="assign[%s,%s]")

m.update()
for key in x:
    print(key, x[key], x[key].Vtype, x[key].lb, x[key].ub)
"""

# Create job constraints
jobs = m.addConstrs((x.sum('*',j) == 1 for j in J), name='job')

"""
for job in J:
    exp = 0
    for res in R:
        #print("x[",(res,job),"]")
        exp += x[(res,job)]
    #print("Sum  == 1")
    m.addConstr(exp == 1, name="hola")
"""

# Create resource constraints
resources = m.addConstrs((x.sum(r,'*') <= 1 for r in R), name='resource')

"""
for res in R:
    exp = 0
    for job in J:
        #print("x[",(res,job),"]")
        exp += x[(res,job)]
    #print("Sum  == 1")
    m.addConstr(exp <= 1)
"""

# Objective: maximize total matching score of all assignments
m.setObjective(x.prod(scores), GRB.MINIMIZE) 

"""
exp = 0
for job in J:
    for res in R:
        exp +=  x[(res,job)]*scores[(res,job)]
m.setObjective(exp, GRB.MAXIMIZE)
"""

# Carlos is the Java Developer
# exp = x[('Carlos','JavaDeveloper')] 
# m.addConstr(exp == 1)

# Save model for inspection
m.write('RAP.lp')

# Run optimization engine
m.optimize()

# Display optimal values of decision variables
for v in m.getVars():
    if v.x > 1e-6:
        print(v.varName, v.x)

# Display optimal total matching score
print('Total matching score: ', m.objVal)