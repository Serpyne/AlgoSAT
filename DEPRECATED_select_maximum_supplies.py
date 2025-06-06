

"""

Deprecated DP method to select supplies from a given order such that the net weight is lower than the full fuel payload of the given plane; akin to the Knapsack Problem

"""


from supply import SupplyOrder, Supplies, SUPPLY_WEIGHT, SUPPLY_COST

CONVERSION_TO_INT = 100

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

    W_scaled = int(W * CONVERSION_TO_INT)
    weights_scaled = [int(w * CONVERSION_TO_INT) for w in weights]

    # 2D table where first column is the maximum value of the given supplies
    # and the second column is its corresponding list of items.
    dp = [[(0.0, Supplies()) for _ in range(W_scaled + 1)] for _ in range(len(weights) + 1)]

    for i in range(1, len(weights) + 1): # Each supply 
        for w in range(1, W_scaled + 1): # Each supply capacity
            
            # Standard case: Do not carry the supply
            dp[i][w] = dp[i - 1][w]

            # Calculate the maximum number that this supply can fit
            max_count = min(counts[i - 1], w // weights_scaled[i - 1])

            # Iterate through [1, 2, ..., max_count]
            for k in range(1, max_count + 1):
                remaining = w - k * weights_scaled[i - 1]
                if remaining >= 0:
                    prev_val, items = dp[i-1][remaining]
                    new_val = prev_val + k * values[i - 1]
                    new_items = items.copy()
                    new_items.add(names[i - 1], k)

                    # Update the table if taking k number of supplies is more optimal
                    if new_val > dp[i][w][0]:
                        dp[i][w] = (new_val, new_items)

    selected_names = dp[len(weights)][W_scaled][1]
    print(dp[len(weights)][W_scaled])

    new_order = order.copy()
    new_order.supplies = selected_names
    remaining_order = order.copy()
    s = selected_names.dict()
    for supply in s:
        count = s[supply]
        remaining_order.supplies.remove(supply, count)

    return new_order, remaining_order

if __name__ == "__main__":
    
    orders = [
        SupplyOrder(town = "Geraldton", supplies = Supplies(dialysismachine = 5, scalpel = 1)),
    ]

    W = 1381.0 # kg
    
    for order in orders:

        new, remaining = select_maximum_of_supplies(W, order)
        print("New Order:", new.supplies)
        print("Remaining Order:", remaining.supplies)
        print(new.net_weight, remaining.net_weight)
        print(new.net_value, remaining.net_value)

