def fractinal_knapsack(values, weights, W):
    n = len(weights)
    ratios = [(values[i]/weights[i], values[i], weights[i]) for i in range(n)]

    # sort the items based in decrasing order
    ratios.sort(reverse=True)

    total_val = 0
    current_weight = 0
    for ratio, val, weight in ratios:
        if current_weight + weight <= W:
            total_val += val
            current_weight += weight
        else:
            fraction = (W-current_weight)/weight
            total_val += fraction*val
            break
    return total_val
import heapq

class node:
    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency
        self.left = None
        self.right = None

def hoff_man():
    pass

if __name__ == "__main__":
    values = [40,50,20]
    weights = [2,5,4]
    W = 6
    print(fractinal_knapsack(values=values,weights=weights,W=W))