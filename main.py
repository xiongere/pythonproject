def can_connect(a, b):
    return (a[1] == 0 and b[0] == 0) or (a[1] + b[0] <= 28 and a[1] + b[0] >= 26)


def dfs(graph, node, visited, result):
    visited[node] = True
    result.append(node)

    for neighbor in graph[node]:
        if not visited[neighbor]:
            dfs(graph, neighbor, visited, result)


def sort_counts(counts):
    # Build a graph to represent connections between elements
    graph = {i: [] for i in range(len(counts))}
    for i in range(len(counts)):
        for j in range(len(counts)):
            if i == j:
                continue
            if can_connect(counts[i], counts[j]):
                graph[i].append(j)

    # Perform DFS to get the sorted order
    visited = [False] * len(counts)
    result = []
    for i in range(len(counts)):
        if not visited[i]:
            dfs(graph, i, visited, result)

    return result[::-1]


if __name__ == "__main__":
    counts = [[0, 14], [24, 0], [0, 0],[37, 0], [0, 0], [0, 8], [0, 2], [0, 21], [6, 0], [18, 0], [12, 58]]
    final = sort_counts(counts)
    print(final)
