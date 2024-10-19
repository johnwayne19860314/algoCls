
function dijkstra(graph, startProduct) {
    let n = graph.length;
    let minDistances = new Array(n).fill(Infinity);
    let visited = new Array(n).fill(false);
    
    minDistances[startProduct] = 0;

    for (let i = 0; i < n; i++) {
        let minIndex = -1;
        for (let j = 0; j < n; j++) {
            if (!visited[j] && (minIndex === -1 || minDistances[j] < minDistances[minIndex])) {
                minIndex = j;
            }
        }
        if (minDistances[minIndex] === Infinity) {
            break;
        }
        visited[minIndex] = true;
        
        for (let j = 0; j < n; j++) {
            if (graph[minIndex][j] !== 0) {
                let potentialDist = minDistances[minIndex] + graph[minIndex][j];
                if (potentialDist < minDistances[j]) {
                    minDistances[j] = potentialDist;
                }
            }
        }
    }
    return minDistances;
}

let graph = [
    [0, 2, 0, 1, 0],
    [2, 0, 3, 0, 0],
    [0, 3, 0, 4, 0],
    [1, 0, 4, 0, 5],
    [0, 0, 0, 5, 0]
];
console.log(dijkstra(graph,0))