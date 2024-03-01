def find_decomposition(budget: list[float], preferences: list[set[int]]) -> dict:
    total_budget = sum(budget)
    num_players = len(budget)

    # Check if the total budget is divisible by the number of players
    if total_budget % num_players != 0:
        return None  # Decomposition is not possible

    # Calculate the share of each player
    player_share = total_budget / num_players

    # Initialize the result dictionary to store the budget allocation for each player
    result = {i: {} for i in range(num_players)}

    # Iterate through each item
    for item in range(len(budget)):
        item_cost = budget[item]

        # Find the players who support the current item
        supporting_players = [player for player, preference in enumerate(preferences) if item + 1 in preference]

        # Divide the cost of the item among supporting players
        share_per_player = item_cost / len(supporting_players) if supporting_players else 0

        # Allocate the share to each supporting player and deduct from their budget
        for player in supporting_players:
            result[player][item + 1] = share_per_player
            budget[player] -= share_per_player

    # Adjust the allocations to ensure that all the budget is utilized
    for player in range(num_players):
        remaining_budget = player_share - sum(result[player].values())
        if remaining_budget > 0:
            result[player][item + 1] += remaining_budget

    return result

# Example usage:
budget = [100, 200, 150]
preferences = [{1, 2}, {2, 3}, {1, 3}]

result = find_decomposition(budget, preferences)
print(result)
