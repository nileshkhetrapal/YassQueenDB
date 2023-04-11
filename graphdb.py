import socket
import threading
import json
from time import sleep

class GraphDatabase:
    def __init__(self):
        self.graph = {}
        self.text_pieces = []

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, node1, node2):
        if node1 in self.graph and node2 in self.graph:
            self.graph[node1].append(node2)
            self.graph[node2].append(node1)

    def remove_edge(self, node1, node2):
        if node1 in self.graph and node2 in self.graph:
            self.graph[node1].remove(node2)
            self.graph[node2].remove(node1)

    def remove_node(self, node):
        if node in self.graph:
            for other_node in self.graph[node]:
                self.graph[other_node].remove(node)
            del self.graph[node]

    def update_from_main(self, new_graph):
        self.graph = new_graph
    
    def store_text_piece(self, text):
        self.text_pieces.append(text)

    def get_all_text_pieces(self):
        return self.text_pieces

    def update_from_main(self, new_graph, new_text_pieces):
        self.graph = new_graph
        self.text_pieces = new_text_pieces


def serve_main_node(graph_db, host, port):
    print("Serving main node at", host, port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    while True:
        conn, addr = server.accept()
        request = conn.recv(1024).decode('utf-8')
        response = ""

        if request.startswith("STORE_TEXT:"):
            text = request[len("STORE_TEXT:"):]
            graph_db.store_text_piece(text)
            response = "TEXT_STORED"
        elif request == "GET_TEXT_PIECES":
            response = json.dumps(graph_db.get_all_text_pieces())
        elif request == "GET_GRAPH":
            response = json.dumps(graph_db.graph)
        else:
            print("Unknown request:", request)

        conn.send(response.encode('utf-8'))
        conn.close()

def update_follower_node(graph_db, host, port):
    while True:
        sleep(5)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        client.send("GET_TEXT_PIECES".encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        new_data = json.loads(response)
        new_graph = new_data["graph"]
        new_text_pieces = new_data["text_pieces"]
        graph_db.update_from_main(new_graph, new_text_pieces)

        client.close()

def check_main_node_availability(host, port, timeout=3):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout)
        client.connect((host, port))
        client.close()
        return True
    except socket.error:
        return False

def switchover_main_node(graph_db, host, port):
    while True:
        sleep(10)
        main_node_ip = get_main_node_ip(host, port)
        if main_node_ip is None:
            print("Main node not available, switching to main node")
            serve_main_node(graph_db, host, port)

def get_main_node_ip(host, port, timeout=3):
    follower_nodes = [follower_node1_ip, follower_node2_ip]
    for node_ip in follower_nodes:
        if node_ip != host:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.settimeout(timeout)
                client.connect((node_ip, port))
                client.send("GET_MAIN_NODE_IP".encode('utf-8'))

                response = client.recv(1024).decode('utf-8')
                main_node_ip = response.strip()
                client.close()

                return main_node_ip
            except socket.error:
                pass

    return None

def main():
    main_node_ip = "10.0.5.201"
    follower_node1_ip = "10.0.5.202"
    follower_node2_ip = "10.0.5.203"

    host = "127.0.0.1"  # This line will be replaced with the appropriate IP address
    port = 6666
    #If the host name is u1-nilesh, then the node is main node
    if socket.gethostname() == "u1-nilesh":
        node_type = "main"
    else:
        node_type = "follower"

    graph_db = GraphDatabase()

    if node_type == "main":
        host = main_node_ip
        serve_main_node(graph_db, host, port)
    elif node_type == "follower":
        host = follower_node1_ip if check_main_node_availability(main_node_ip, port) else follower_node2_ip

        update_thread = threading.Thread(target=update_follower_node, args=(graph_db, main_node_ip, port))
        update_thread.start()

        switchover_thread = threading.Thread(target=switchover_main_node, args=(graph_db, host, port))
        switchover_thread.start()
    else:
        print("Invalid node type")

if __name__ == "__main__":
    main()

