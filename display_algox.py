from taxicab_distances import *
import algorithmx

server = algorithmx.http_server(port=5050)
graph = server.canvas()
graph.edgelayout('individual')

node_config = {"shape": "rect", "size": [23, 8], "labels": {}}

def main():
    
    nodes = generate_nodes()
    edges = generate_edges()

    graph.nodes(nodes).add(shape="rect", size=(45, 8))
    graph.edges(edges).add(labels=lambda e: {0: {"text": edges[e]}})
    
    graph.pause(1)

    graph.nodes(nodes).fixed(True)

if __name__ == "__main__":
    config = node_config.copy()
    print("localhost:5050")
    graph.onmessage('start', main)
    server.start()