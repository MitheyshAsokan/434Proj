from gurobipy import * 
import random as rand
import csv


m = Model("mip1")

## sets
M = 30
N = 30
K = 5
G = N

PRODUCTS = [i+1 for i in range(K)]
SELLERS = [i+1 for i in range(M)]
BUYERS = [i+1 for i in range(N)]

ORDERS = [i+1 for i in range(G)]
ORDERS_LIST = []

for i in range(G):
    order = {}
    for k in PRODUCTS:
        order[k] = rand.randint(0, 1000)
    ORDERS_LIST.append(order)


BUYER_SURPLUS = {}
for j in BUYERS:
    prods = []
    for k in PRODUCTS:
        include = rand.randint(0,1)
        if (include == 1):
            prods.append(k)
    BUYER_SURPLUS[j] = prods

print("Buyer's Surplus: \n\n")
print(BUYER_SURPLUS)
print("\n\n")

# i: [price_k1, ...]
SELLER_SURPLUS = {}
for i in SELLERS:
    price = []
    for k in range(K):
        price.append(rand.randint(1, 5))
    SELLER_SURPLUS[i] = price

print("Seller's Surplus: \n\n")
print(SELLER_SURPLUS)
print("\n\n")

def a(S, k):
    return S[k]

def vi(S, i):
    total = 0
    for k, count in S.items():
        total += count*SELLER_SURPLUS[i][k-1]
    return total

def vj(S, j):
    total = 0
    for k, count in S.items():
        if (k in BUYER_SURPLUS[j]):
            total += count*5
    return total

def S(k):
    result = []
    for index, S in enumerate(ORDERS_LIST):
        if S[k] > 0:
            result.append(index)
    return result

# Decision Variables
x = m.addVars(ORDERS, BUYERS, vtype=GRB.BINARY, name="x") # BUYERS
y = m.addVars(ORDERS, SELLERS, vtype=GRB.BINARY, name="y") # SELLERS

# Objective
obj = sum([vj(ORDERS_LIST[s_index -1 ], j)*x[s_index, j] for s_index in ORDERS for j in BUYERS]) + sum([vi(ORDERS_LIST[s_index-1], i)*y[s_index, i] for s_index in ORDERS for i in SELLERS])

#Constraints
m.addConstrs((y.sum(i, '*') <= 1 for i in SELLERS), "(1) Only one Seller per Item set")
for k in PRODUCTS:
    m.addConstr(sum([x[s_index+1, j]*a(ORDERS_LIST[s_index], k) for j in BUYERS for s_index in S(k)]) <= sum([y[s_index+1, i]*a(ORDERS_LIST[s_index], k) for i in SELLERS for s_index in S(k)]), "(1) Buyer cannot get more K than available")

# m.update()

m.setObjective(obj, GRB.MAXIMIZE)

m.optimize()
print("Selected \n")
for v in m.getVars():
    if v.x == 1:
        print('%s %g' % (v.varName, v.x))
print("\n")

print("All \n")
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))
print("\n")