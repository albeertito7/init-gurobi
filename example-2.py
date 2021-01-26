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
# Carlos is the Java Deveolper
m.addConstr((x[('Carlos', 'JavaDeveloper')] == 1) , name="carlosJava") ## we want that carlos be the javadeveloper
"""

"""
for res in R:
    exp = 0 # an expression, will become our constraint (a linear combination)
    for job in J:
        #print("x[", (res, job),"]")
        exp += x[(res, job)] #summing the columns
    print("Sum == 1")
    m.addConstr(exp == 1, name="asdf")
"""

# Create resource constraints
resources = m.addConstrs((x.sum(r,'*') <= 1 for r in R), name='resource')

# Objective: maximize total matching score of all assignments
m.setObjective(x.prod(scores), GRB.MINIMIZE) # GRB.MINIMIZE # objective functions

"""
exp = 0
for job in J:
    for res in R:
        exp += x[(res,job)]*scores[(res, job)]
m.setObjective(exp, GRB.MAXIMIZE)
"""

## now we have a model with all the variables and the constraints

# Save model for inspection
m.write('RAP.lp') #there are multiple formalims -> RAP.lp, RAP.ms ... etc

# Run optimization engine
m.optimize()


# Display optimal values of decision variables
for v in m.getVars(): ## at any point u can get the vars
    if v.x > 1e-6: # v.x accessing the value of the variable ## this if is because of precision guroby problems #compare to see if the v.x is bigger than zero
        print(v.varName, v.x)

# Display optimal total matching score
print('Total matching score: ', m.objVal)