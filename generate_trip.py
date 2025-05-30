"""
subroutine determine_route
Inputs:
- F: Max fuel capacity
- W0: Weight of plane without any inventory or fuel on-board
- C: Full fuel payload capacity of plane
- source: [optional]
- orders'list': List of SupplyOrder(s) (A custom ADT containing town and supplies). 
"""

from typing import Union
from math import log, exp

from taxicab_distances import generate_nodes, generate_edges
from supply import SupplyOrder, Supplies
from constants import C1, C2, UFV1, UFV2, EMPTY_WEIGHT_1, EMPTY_WEIGHT_2, MARKET_FUEL_COST_PER_LITRE, SMALLER_PLANE, LARGER_PLANE
from select_maximum_supplies import select_maximum_of_supplies

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

def determine_route(F: int, W0: int, source: str = "Perth",  orders: list[SupplyOrder] = None) -> Union[list[str], list[int], list[list[SupplyOrder]], int, int]:

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
    path_orders.append(None)

    fuel_usage = f(path[-2], path[-1], W0)
    fT += fuel_usage
    path_fuel_usages.append(fuel_usage)

    return path, path_fuel_usages, path_orders, fT, W, orders

def display(path_orders, path_fuel_usages, C):
    net_value: float = 0
    net_expenses = fT * MARKET_FUEL_COST_PER_LITRE
    net_weight: float = 0
    
    output_lines: list[tuple] = [
        ("Plane", plane),
        ("Initial Payload", ""),
        ("Full Fuel Payload", f"{float(C):.3f} kg"),
        ("Fuel Capacity", f"{float(F):.2f} L"),
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
            if order is None: n += 1; continue
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
            elif "Initial Payload" in s:     args = f"{net_weight:.3f} kg"
            print(f"{s} {args}")
            continue

        print(s)
        n = 1
        while n < len(path) - 1:
            order: SupplyOrder = path_orders[n - 1]
            if order is None: n += 1; continue
            print(f"{n}.   {order.town}")
            print(f"{(lead_spacing + 'Weight:').ljust(trailing_padding)}    {order.supplies.net_weight:.3f} kg")
            print(f"{(lead_spacing + 'Value:').ljust(trailing_padding)}    {order.supplies.net_value:.2f} AUD")
            print(f"{(lead_spacing + 'Fuel Usage:').ljust(trailing_padding)}    {path_fuel_usages[n - 1]:.2f} L")
            print(f"{(lead_spacing + 'Supplies:').ljust(trailing_padding)}    {order.supplies}")

            n += 1
        
        print(f"{n}.   Perth (Refuel Destination)")
        print(f"{'      Fuel Usage:'.ljust(trailing_padding)}    {path_fuel_usages[n - 1]:.2f} L")

    print()

if __name__ == "__main__":

    orders = [
        SupplyOrder(town = "Exmouth", supplies = Supplies(stitches = 10)),
        SupplyOrder(town = "Monkey Mia", supplies = Supplies(dialysismachine = 20)),
        SupplyOrder(town = "Broome", supplies = Supplies(nitrousoxidecanister = 30)),
        SupplyOrder(town = "Derby", supplies = Supplies(soap = 40)),
        SupplyOrder(town = "Esperance", supplies = Supplies(scalpel = 50)),
        SupplyOrder(town = "Wyndham", supplies = Supplies(syringe = 60)),
        SupplyOrder(town = "Albany", supplies = Supplies(masks = 70)),
        SupplyOrder(town = "Port Hedland", supplies = Supplies(vaccinationkit = 80)),
        SupplyOrder(town = "Fitzroy Crossing", supplies = Supplies(stethoscope = 90)),
        SupplyOrder(town = "Halls Creek", supplies = Supplies(bandages = 100)),
        SupplyOrder(town = "Geraldton", supplies = Supplies(sanitiser = 110)),
    ]
    
    previous_plane = LARGER_PLANE

    added_count = 0
    for i, order in enumerate(orders.copy()):
        C = [C1, C2][int((i + added_count + int(previous_plane == SMALLER_PLANE)) % 2)]
        if order.net_weight > C:
            i += added_count

            order = orders[i]
            new, remainder = select_maximum_of_supplies(C, order)
            orders[i] = new
            orders.insert(i + 1, remainder)
            added_count += 1

    while len(orders) > 0:
        if previous_plane == LARGER_PLANE:
            previous_plane = SMALLER_PLANE
            plane = "Small"
            F = UFV1
            C = C1
            EW = EMPTY_WEIGHT_1
        else:
            previous_plane = LARGER_PLANE
            plane = "Large"
            F = UFV2
            C = C2
            EW = EMPTY_WEIGHT_2

        path, path_fuel_usages, path_orders, fT, W, orders = determine_route(F = UFV1,
                                                                             W0 = EW,
                                                                             orders=orders)

        # Display the final route to you, the Flight Discharge Officer.
        display(path_orders, path_fuel_usages, C)