

def a_star_search(start, end):
    open_list = [start]
    came_from = {start: None}
    total_running_cost = {start: 0}
    path = []

    while len(open_list) > 0:
        current_road = open_list[0]
        open_list.remove(current_road)
        if current_road == end:
            break
        for next_road in current_road.get_connected():
            cost = total_running_cost[current_road] + current_road.cost_to_road(next_road)
            current_road.cost_to_goal = cost
            if next_road not in total_running_cost or cost < total_running_cost[next_road]:
                total_running_cost[next_road] = cost
                open_list.append(next_road)
                open_list.sort(key=lambda x: x.cost_to_road, reverse=True)
                came_from[next_road] = current_road

    path_node = end
    while path_node != start:
        path.append(path_node.name)
        path_node = came_from[path_node]
    path.append(start.name)
    path.reverse()

    return path
