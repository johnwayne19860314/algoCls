# Initialize graph with infinity representing no direct path
INF = float('inf')

# Example graph as an adjacency matrix for 7 nodes (A to G)
# Node layout:
# A -> B = 3, A -> D = 7
# B -> C = 2
# C -> G = 5, C -> D = 1
# D -> A = 2, D -> F = 4
# E -> F = 6
# F -> G = 3
graph = [
    [0, 3, INF, 7, INF, INF, INF],   # A
    [INF, 0, 2, INF, INF, INF, INF], # B
    [INF, INF, 0, 1, INF, INF, 5],   # C
    [2, INF, INF, 0, INF, 4, INF],   # D
    [INF, INF, INF, INF, 0, 6, INF], # E
    [INF, INF, INF, INF, INF, 0, 3], # F
    [INF, INF, INF, INF, INF, INF, 0]# G
]

# Floyd-Warshall algorithm
def floyd_warshall(graph):
    # Number of vertices
    V = len(graph)
    
    # Distance matrix to store shortest paths
    dist = [row[:] for row in graph]  # Copy the initial distances from graph

    # Update distances using intermediate vertices
    for k in range(V):
        for i in range(V):
            for j in range(V):
                # Check if going through vertex k is shorter
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # Print the result
    print("Shortest distances between every pair of vertices:")
    for i in range(V):
        for j in range(V):
            if dist[i][j] == INF:
                print("INF", end="\t")
            else:
                print(dist[i][j], end="\t")
        print()

# Run the algorithm
floyd_warshall(graph)