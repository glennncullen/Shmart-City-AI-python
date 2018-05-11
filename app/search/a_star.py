from Queue import PriorityQueue


def a_star_search(start, end):
    queue = PriorityQueue()
    queue.put(start, 0)
    came_from = {start: None}
    total_running_cost = {start: 0}
    path = []

    while not queue.empty():
        current_road = queue.get()
        if current_road == end:
            break
        for next_road in current_road.get_connected():
            cost = total_running_cost[current_road] + current_road.cost_to_road(next_road)
            if next_road not in total_running_cost or cost < total_running_cost[next_road]:
                total_running_cost[next_road] = cost
                queue.put(next_road, cost)
                came_from[next_road] = current_road

    path_node = end
    while path_node != start:
        path.append(path_node.name)
        path_node = came_from[path_node]
    path.append(start.name)
    path.reverse()

    return path
