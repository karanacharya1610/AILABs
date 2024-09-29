import random
def generateInstance(n, k, m):

  vars = []
  for i in range(n):
    vars.append((chr(i + 65)))

  problem = "(("
  clause = []

  for i in range(k * m):

    x = random.choice(vars)
    vars.remove(x)
    clause.append(x)

    if(i % k == k - 1):
      while len(clause) != 0:
        vars.append(clause.pop(0))

    y = random.random()
    if y < 0.5:
      problem += "~"
    
    problem += x

    if i % k == k - 1 and i != (k * m - 1):
      problem += ") and ("
    elif i != (k * m - 1):
      problem += " or "
  
  problem += "))"
      
  return problem
for i in range(10):
  print("Problem ", i+1, ": ", generateInstance(12, 3, 4))