import osmnx as ox  # for the graphing and driving map capabilities
import random  # for random.choice() in the list of nodes
import ctypes  # for our message box
import threading  # to display warning and map at once with multi threading


# download/model a street network for some city then visualize it
G = ox.graph_from_place("Cuyahoga Falls, Ohio, USA", network_type="drive")

# impute missing edge speeds and calculate edge travel times with the speed module, for ox.shortest_path
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

# generate our random routes by selecting 4 random nodes on the graph
randomNodeList = []
for i in range(4):
    randomNodeList.append(random.choice(list(G.nodes())))

# create our two routes with ox.shortest_path and the randomNodeList made above, done by travel time
routes = [ox.shortest_path(G, randomNodeList[0], randomNodeList[1], weight="travel_time"),
          ox.shortest_path(G, randomNodeList[2], randomNodeList[3], weight="travel_time")]

# convert routes to geodataframes (gdfs)
route_gdfs = ox.graph_to_gdfs(G, nodes=True, edges=False)
# reindex to the routes specifically and reset index
routeNodes = route_gdfs.reindex(routes[0]).reset_index()
route2Nodes = route_gdfs.reindex(routes[1]).reset_index()

# merge the two graphs based on x
m = routeNodes.merge(route2Nodes, on='x')

# for our warning message thread
def warnUser():
    ctypes.windll.user32.MessageBoxW(0,
                                     "Your route is on course with an emergency service vehicle, stay alert and yield!",
                                     "WARNING!", 1)


# if any of the y's are equal we got an intersection
if (m['y_x'] == m['y_y']).any():
    #print("intersect!")
    threading.Thread(target=warnUser).start()  # multi thread a warning so can see map and warning
else:
    print("do not intersect...")

fig, ax = ox.plot_graph_routes(G, routes, node_size=0)  # then graph it
