def find_decomposition(itemCost: list[float], preferences: list[set[int]]) -> dict:
    total_budget = sum(itemCost)
    num_players = len(preferences)

    budget_players = [total_budget // num_players] * len(preferences)


    # Initialize the result dictionary to store the budget allocation for each player
    result = {i: {} for i in range(num_players)}


    # Iterate through each item
    for item in range(len(itemCost)):
        item_cost = itemCost[item]

        # Find the players who support the current item, excluding those with zero budgets
        supporting_players = [player for player, preference in enumerate(preferences) if item in preference and budget_players[player] > 0]

        # Divide the cost of the item among supporting players
        share_per_player = item_cost / len(supporting_players) if supporting_players else "Not decomposition"

        # Allocate the share to each supporting player and deduct from their budget
        for player in supporting_players:
            result[player][item] = share_per_player

            # Deduct from budget only if the player has a non-zero budget
            if budget_players[player] > 0:
                budget_players[player] -= share_per_player

    return result

# Example usage:
itemCosts = [100, 200, 150]
preferences = [{0, 1}, {1, 2}, {0, 2}]

result = find_decomposition(itemCosts, preferences)
print(result)

itemCosts = [400, 50, 50, 0]
preferences = [{0, 1}, {0, 2}, {0, 3}, {1, 2}, {0}]

result = find_decomposition(itemCosts, preferences)
print(result)
