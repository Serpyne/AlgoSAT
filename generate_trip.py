"""
Inputs:
- ~~Destination (T)~~ (OMITTED)
- Edge weights (Distance between destination)
- Orders [Location, Net Weight]
"""

from typing import Union
from math import log, exp

from taxicab_distances import generate_nodes, generate_edges
from supply import SupplyOrder, Supplies
from constants import C1, C2, UFV1, UFV2, EMPTY_WEIGHT_1, EMPTY_WEIGHT_2, MARKET_FUEL_COST_PER_LITRE

nodes = generate_nodes()
edges = generate_edges()

def neighbours(node) -> list[str]:
    n = []
    for edge in edges:
        if edge[0] == node:
            n.append(edge[1])
        elif edge[1] == node:
            n.append(edge[0])
    return n

def f(u, v, W: int) -> int:
    """
    Returns fuel usage from node u to node v.
    Parameters:
    - node pair(u, v)
    - W: weight of inventory
    """

    s = (u, v)

    # Pull distance between u and v
    D = 0
    if s in edges:
        D = edges[s]
    if s[::-1] in edges:
        D = edges[s[::-1]]

    if D == 0: return 0

    # Arbitrary fuel usage equation
    fuel_usage = W * (log(D + 1) + exp(-D) - 1) * .02

    return fuel_usage

def choose_order_index_by_town(orders: list[SupplyOrder], town: str) -> int:

    for i in range(len(orders)):
        if orders[i].town == town:
            return i
    return None

def determine_route(F: int, W0: int, C: int, source: str = "Perth",  orders: list[SupplyOrder] = None) -> Union[list[str], list[int], list[list[SupplyOrder]], int, int]:

    if orders is None:
        print("No orders today - You can go off work!")
        return

    path: list[str]                      = [source]  # Circuit of nodes
    path_fuel_usages: list[int]          = []        # Fuel Usage between adjacent towns
    path_orders: list[list[SupplyOrder]] = []        # Keep the sequence of orders when traversing

    fT: int                              = 0         # Total fuel consumed
    T: None | str                        = None      # Target/Destination
    
    W = 0                                            # Net weight of order
    for order in orders:
        W += order.net_weight
    
    while len(path) <= len(nodes):

        if path[-1] == T:
            break

        T = path[-1]

        # Iteratively find smallest edge not already in the circuit.

        fmin = float('inf')     # Min fuel
        Wmin = None             # Min weight
        Tmin = None             # Min destination
        order_index = None      # Order index of the min destination

        towns_in_order_list = [order.town for order in orders]

        for v in neighbours(T):
            if v in path: continue
            if v not in towns_in_order_list: continue

            aux = f(T, v, W0 + W)

            # Stores order index through memoisation to avoid calling choose_order_index_by_town(...) more than once. 
            i = choose_order_index_by_town(orders, v)
            delta_W = orders[i].net_weight
            NEW_W = W - delta_W
            rem = f(v, source, W0 + NEW_W)

            if W > C:
                
                continue

            if fT + aux + rem > F: continue

            if aux >= fmin: continue

            fmin = aux
            Tmin = v
            Wmin = delta_W
            order_index = i

        # Add closest (unvisited) neighbour to circuit and add the weight to the total fuel consumed.

        if Tmin is not None:
            path.append(Tmin)
            fT += fmin
            W -= Wmin
            path_fuel_usages.append(fmin)
            path_orders.append(orders.pop(order_index))

    # Complete the circuit by appending the source node 
    path.append(source)

    fuel_usage = f(path[-2], path[-1], W0)
    fT += fuel_usage
    path_fuel_usages.append(fuel_usage)

    return path, path_fuel_usages, path_orders, fT, W

if __name__ == "__main__":
    plane = "Small"
    F = UFV1

    path, path_fuel_usages, path_orders, fT, W = determine_route(F = UFV1, W0 = EMPTY_WEIGHT_1, C = C1,
                                                                 orders=[
        # SupplyOrder(town = "Esperance", supplies = Supplies(scalpel = 1)),
        SupplyOrder(town = "Geraldton", supplies = Supplies(dialysismachine = 10)),
        # SupplyOrder(town = "Monkey Mia", supplies = Supplies(stitches = 100, sticker = 10000)),
        # SupplyOrder(town = "Wyndham", supplies = Supplies(dialysismachine = 1)),
        # SupplyOrder(town = "Broome", supplies = Supplies(sticker = 500)),
    ])
    
    # Display the final route to you, the Flight Discharge Officer.

    net_value: float = 0
    net_expenses = fT * MARKET_FUEL_COST_PER_LITRE
    net_weight: float = 0
    
    output_lines: list[tuple] = [
        ("Plane", plane),
        ("Initial Payload", ""),
        ("Full Fuel Payload", f"{float(C1)} kg"),
        ("Fuel Capacity", f"{float(F)} L"),
        ("Flight Route (Beginning at Perth)", ()),
        ("Total Fuel Consumed", f"{fT:.2f} L"),
        ("Net Order Value", ""),
        ("Market Fuel Cost", f"{MARKET_FUEL_COST_PER_LITRE} AUD/L"),
        ("Net Expenses", f"{net_expenses:.2f} AUD"),
        ("Net Profit", ""),
    ]

    lead_spacing = " " * 10
    
    # Determine longest-length heading for display padding.
    trailing_padding = 0
    for heading, _ in output_lines:
        if len(heading) > trailing_padding:
            trailing_padding = len(heading)

    for i, line in enumerate(output_lines):
        heading, args = line

        if type(args) != tuple:
            output_lines[i] = (heading, args)
            continue

        n = 1
        while n < len(path) - 1:
            order: SupplyOrder = path_orders[n - 1]
            net_value += order.supplies.net_value
            net_weight += order.supplies.net_weight
            n += 1
        
    print()
    for i, line in enumerate(output_lines):
        heading, args = line

        heading += ":"
        s = ""
        s += heading.ljust(trailing_padding + 3)

        if type(args) != tuple:
            if "Value" in s:        args = f"{net_value:.2f} AUD"
            elif "Profit" in s:     args = f"{net_value - net_expenses:.2f} AUD"
            elif "Initial Payload" in s:     args = f"{net_weight:.2f} kg"
            print(f"{s} {args}")
            continue

        print(s)
        n = 1
        while n < len(path) - 1:
            order: SupplyOrder = path_orders[n - 1]
            print(f"{n}.   {order.town}")
            print(f"{(lead_spacing + 'Weight:').ljust(trailing_padding)}    {order.supplies.net_weight:.2f} kg")
            print(f"{(lead_spacing + 'Value:').ljust(trailing_padding)}    {order.supplies.net_value:.2f} AUD")
            print(f"{(lead_spacing + 'Fuel Usage:').ljust(trailing_padding)}    {path_fuel_usages[n - 1]:.2f} L")
            print(f"{(lead_spacing + 'Supplies:').ljust(trailing_padding)}    {order.supplies}")

            n += 1
        
        print(f"{n}.   Perth (Refuel Destination)")
        print(f"{'      Fuel Usage:'.ljust(trailing_padding)}    {path_fuel_usages[n - 1]:.2f} L")

    print()
