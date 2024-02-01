import osmnx as ox  # for the graphing and driving map capabilities
import random  # for random.choice() in the list of nodes
import tkinter  # gui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # for displaying on our gui

# our basic gui
root = tkinter.Tk()
root.title("Swifter Sirens Simulation")


# download/model a street network for some city then visualize it
G = ox.graph_from_place("Cuyahoga Falls, Ohio, USA", network_type="drive")

# impute missing edge speeds and calculate edge travel times with the speed module, for ox.shortest_path
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

fig, ax = ox.plot_graph(G, node_size=0, show=False)  # then graph it
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, padx=20, pady=20)


def randomRouteCheck():
    global canvas_widget

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

    fig, ax = ox.plot_graph_routes(G, routes, node_size=0, show=False)  # then graph it

    # Embed the plot into Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, padx=20, pady=10)

    # if any of the y's are equal we got an intersection
    if (m['y_x'] == m['y_y']).any():
        tkinter.messagebox.showwarning(title="WARNING!", message="Your route is on course with an emergency service vehicle, stay alert and yield!")
    # else:
        # print("do not intersect...")


btn = tkinter.Button(root, text = 'Generate Routes', bd = '5',
                          command = randomRouteCheck)
btn.grid(row=1, column=0, pady=10)

root.mainloop()