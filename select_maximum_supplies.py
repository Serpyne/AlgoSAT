"""

DP approach to select supplies from a given order to fit under the max full fuel payload of a given plane.
This is an upgrade from the previous deprecated version.

"""


from supply import SupplyOrder, Supplies, SUPPLY_WEIGHT, SUPPLY_COST

def select_maximum_of_supplies(W: float, order: SupplyOrder):
    """
    W: maximum capcity/weight in kg
    order: {supplies: count}

    Returns the SupplyOrder ADT of SupplyOrder{town = "...", supplies = selected_count}.
    """

    supplies = order.dict()

    names = list(supplies.keys())
    counts = list(supplies.values())
    weights = [SUPPLY_WEIGHT[supply] for supply in names]
    values = [SUPPLY_COST[supply] for supply in names]
    n = len(weights)

    def dfs(capacity: float, idx: int, selected: Supplies, memo: dict = {}):
        # Use a tuple for memoization key (capacity and idx)
        # Round function to avoid floating point precision issues in key
        key = (round(capacity, 6), idx) 
        if key in memo:
            return memo[key]
        if idx == n or capacity <= 0:
            return (0.0, selected.copy())
        
        # Option 1: Skip current item
        max_val, best_selected = dfs(capacity, idx + 1, selected)

        # Option 2: Try to take 1 to counts[idx] of current item
        max_take = min(counts[idx], int(capacity / weights[idx])) if weights[idx] > 0 else 0
        for k in range(1, max_take + 1):
            rem_cap = capacity - k * weights[idx]
            if rem_cap >= 0:
                new = selected.copy()
                name = "".join(names[idx].lower().split())
                if names[idx] in new:
                    new[name] += k
                else:
                    new[name] = k
                val, sel = dfs(rem_cap, idx + 1, new)
                if val + k * values[idx] > max_val:
                    max_val = val + k * values[idx]
                    best_selected = sel.copy()

        memo[key] = (max_val, best_selected)
        return (max_val, best_selected)

    max_value, selected_names = dfs(W, 0, {})

    remaining_order = order.copy()
    new_order = order.copy()
    new_order.supplies._supplies.clear()
    new_order.supplies.net_weight = 0
    for supply in selected_names:
        count = selected_names[supply]
        new_order.supplies.add(supply, count)
        remaining_order.supplies.remove(supply, count)

    return new_order, remaining_order

if __name__ == "__main__":

    order = SupplyOrder(town = "Geraldton", supplies = Supplies(dialysismachine = 15, scalpel = 1))

    W = 1381.0 # kg
    
    new, remaining = select_maximum_of_supplies(W, order)
    print("New Order:", new.supplies)
    print("Remaining Order:", remaining.supplies)
    print(order.net_weight, new.net_weight)
    print(order.net_weight, remaining.net_weight)