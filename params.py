import random as rand
import csv

## sets
M = 20
N = 20
K = 5
G = N

PRODUCTS = [i+1 for i in range(K)]
SELLERS = [i+1 for i in range(M)]
BUYERS = [i+1 for i in range(N)]

ORDERS = [i+1 for i in range(G)]
ORDERS_LIST = []
def order_list(): 
    for i in range(G):
        order = {}
        for k in PRODUCTS:
            order[k] = rand.randint(0, 1000)
        ORDERS_LIST.append(order)

    keys = ORDERS_LIST[0].keys()
    with open('orders_list.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(ORDERS_LIST)

def buyer_surplus():
    BUYER_SURPLUS = {}
    for j in BUYERS:
        prods = []
        for k in PRODUCTS:
            include = rand.randint(0,1)
            if (include == 1):
                prods.append(k)
        BUYER_SURPLUS[j] = prods

    keys = BUYER_SURPLUS.keys()
    with open('buyer_surplus.csv', 'w', newline='')  as output_file:
        dict_writer = csv.writer(output_file)
        dict_writer.writerow(keys)
        for prod in BUYER_SURPLUS.values():
            dict_writer.writerow(','.join(map(str, prod)))

buyer_surplus()