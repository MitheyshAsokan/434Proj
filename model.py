from gurobipy import * 

m = Model("mip1")

## sets
PRODUCTS = [1,2,3,4]
SELLERS = [1,2,3,4,5]
BUYERS = [1,2,3,4,5]

G = [
    {
        "items": {
            1:10,
            2:3,
            3:2,
        }
    },
    {
        "items": {
            1:10,
            2:3,
            4:1
        }
    },
    {
        "items": {
            2:3,
            3:2,
            4:1
        }
    },
    {
        "items": {
            1:10,
            2:3,
            3:2,
            4:1
        }
    },
    {
        "items": {
            1:10,
            2:3
        }
    }
    ]

BUYER_SURPLUS = {
    1: set([1,2,3]),
    2: set([1,2,4]),
    3: set([1,3,5]),
    4: set([1,2,4]),
    5: set([1,3,4])
}

# i: [price_k1, ...]
SELLER_SURPLUS = {
    1: [10, 5, 3, 5],
    2: [5, 3, 1, 6],
    3: [1, 2, 8, 5],
    4: [1, 1, 11, 2],
    5: [1, 1, 1, 12]
}

## parameters
# s_ik - supply
# d_jk - demand
# p_jk - buyer price ub
# p_ik - seller price lb
# C_ij - fixed cost

def a(S, k):
    return S["items"][k]

def vi(S, i):
    total = 0
    for k, count in S["items"].items():
        total += count*SELLER_SURPLUS[i][k-1]
    return total

def vj(S, j):
    total = 0
    for k, count in S["items"].items():
        if (k in BUYER_SURPLUS[j]):
            total += count*5
    return total

def S(k):
    result = []
    for index, S in enumerate(G):
        if k in S["items"].keys():
            result.append(index)
    return result

# Decision Variables
x = m.addVars(BUYERS, BUYERS, vtype=GRB.BINARY, name="x") # BUYERS
y = m.addVars(SELLERS, SELLERS, vtype=GRB.BINARY, name="y") # SELLERS

# Objective
obj = sum([vj(G[s_index], j)*x[s_index + 1, j] for s_index in range(len(G)) for j in BUYERS]) - sum([vi(G[s_index], i)*y[s_index + 1, i] for s_index in range(len(G)) for i in SELLERS])

#Constraints
m.addConstrs((y.sum('*', s_index+1) <= 1 for s_index in range(len(G))), "(1) Only one Seller per Item set")
for k in PRODUCTS:
    m.addConstr((x.sum(s_index+1, j)*a(G[s_index], k) for j in BUYERS for s_index in S(k)) <= (y.sum(s_index+1, i)*a(G[s_index], k) for i in SELLERS for s_index in S(k)), "(1) Buyer cannot get more K than available")

m.update()

m.setObjective(obj, GRB.MAXIMIZE)

m.optimize()