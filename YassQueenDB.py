import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigsh
from scipy.spatial.distance import cosine
import tensorflow as tf
import tensorflow_hub as hub
import os
import pickle

class GraphDatabase:
    def __init__(self):
        self.graphs = {}
        self.current_graph = None
        self.encoder = None

    def load_sentence_encoder(self, model_url='https://tfhub.dev/google/universal-sentence-encoder/4'):
        # Define the YassQueenDB directory
        yqdb_dir = os.path.join(os.path.expanduser('~'), '.yqdb')
        model_name = 'universal_sentence_encoder'

        # Check if YassQueenDB directory exists; if not, create it
        if not os.path.exists(yqdb_dir):
            os.makedirs(yqdb_dir)

        # Check if the model exists in the YassQueenDB directory
        model_path = os.path.join(yqdb_dir, model_name)
        if not os.path.exists(model_path):
            print("Downloading the model...")
            self.encoder = hub.load(model_url)
            tf.saved_model.save(self.encoder, model_path)
            print("Model saved to", model_path)
        else:
            print("Loading the model from", model_path)
            self.encoder = hub.load(model_path)
        
        print("Sentence encoder loaded.")

    def generate_embedding(self, text):
        if self.encoder is not None:
            embedding = self.encoder([text])[0].numpy()
            return embedding
        else:
            print("Sentence encoder not loaded. Please load it first.")
            return None

    def add_node(self, data, relationship=None, to_node=None):
        # Use ALFG to generate a random number for the node name
        seed = np.random.randint(0, 1000)
        rand = np.random.default_rng(seed=seed)
        node_name = str(rand.integers(1, 1_000_000))

        if self.current_graph is not None:
            if node_name not in self.current_graph.nodes:
                # Generate an embedding for the node
                embedding = self.generate_embedding(data)

                # Add the node with the embedding and data as properties
                self.current_graph.add_node(node_name, embedding=embedding, data=data)
                print(f"Node '{node_name}' added to the graph.")

                # If relationship and to_node are provided, add an edge
                if relationship is not None and to_node is not None:
                    self.add_edge(node_name, to_node, relationship)
            else:
                print(f"Node '{node_name}' already exists in the graph.")
        else:
            print("No graph selected. Please create or select a graph first.")
        return node_name

    def create_graph(self, graph_name):
        self.graphs[graph_name] = nx.DiGraph()
        self.current_graph = self.graphs[graph_name]
        print(f"Graph '{graph_name}' created and selected as the working graph.")

    def select_graph(self, graph_name):
        if graph_name in self.graphs:
            self.current_graph = self.graphs[graph_name]
            print(f"Graph '{graph_name}' selected as the working graph.")
        else:
            print(f"Graph '{graph_name}' not found.")

    def add_edge(self, node1, node2, relationship):
        if self.current_graph is not None:
            self.current_graph.add_edge(node1, node2, relationship=relationship)
            print(f"Relationship '{relationship}' added between '{node1}' and '{node2}'.")
        else:
            print("No graph selected. Please create or select a graph first.")

    def delete_node(self, node):
        if self.current_graph is not None:
            if node in self.current_graph.nodes:
                self.current_graph.remove_node(node)
                print(f"Node '{node}' removed from the graph.")
            else:
                print(f"Node '{node}' not found in the graph.")
        else:
            print("No graph selected. Please create or select a graph first.")

    def search_node(self, node):
        if self.current_graph is not None:
            if node in self.current_graph.nodes:
                print(f"Node '{node}' found in the graph.")
            else:
                print(f"Node '{node}' not found in the graph.")
        else:
            print("No graph selected. Please create or select a graph first.")

    def show_graph(self):
        if self.current_graph is not None:
            print("Nodes:")
            for node in self.current_graph.nodes:
                print(f"  {node}")
                #Print the node data
                for key, value in self.current_graph.nodes[node].items():
                    print(f"    {key}: {value}")
            print("\nEdges:")
            for edge in self.current_graph.edges(data=True):
                print(f"  {edge[0]} --({edge[2]['relationship']})--> {edge[1]}")
        else:
            print("No graph selected. Please create or select a graph first.")
    
    def laplacian_eigenmaps(self, k=2):
        if self.current_graph is not None:
            # Convert the directed graph to an undirected graph
            undirected_graph = self.current_graph.to_undirected()

            # Get the Laplacian matrix
            laplacian = nx.laplacian_matrix(undirected_graph).asfptype()

            # Calculate eigenvalues and eigenvectors
            if k < laplacian.shape[0]:
                _, eigenvectors = eigsh(laplacian, k=k, which="SM")
            else:
                _, eigenvectors = eigsh(laplacian.todense())

            # Normalize eigenvectors
            eigenvectors_normalized = eigenvectors / np.linalg.norm(eigenvectors, axis=1)[:, np.newaxis]

            return eigenvectors_normalized
        else:
            print("No graph selected. Please create or select a graph first.")
            return None

    
    def semantic_search(self, query, top_k=1):
        if self.current_graph is not None:
            query_embedding = self.generate_embedding(query)

            if query_embedding is not None:
                distances = [cosine(query_embedding, self.current_graph.nodes[node]['embedding']) for node in self.current_graph.nodes]
                sorted_indices = np.argsort(distances)[:top_k]

                return [(list(self.current_graph.nodes)[i], self.current_graph.nodes[list(self.current_graph.nodes)[i]]['data']) for i in sorted_indices]
            else:
                return []
        else:
            print("No graph selected. Please create or select a graph first.")
            return []

    def save_graph_to_file(self, file_path):
        if self.current_graph is not None:
            with open(file_path, 'wb') as file:
                pickle.dump(self.current_graph, file)
            print(f"Graph saved to '{file_path}'.")
        else:
            print("No graph selected. Please create or select a graph first.")

    def load_graph_from_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                loaded_graph = pickle.load(file)

            # Set the loaded graph as the current graph
            self.current_graph = loaded_graph
            print(f"Graph loaded from '{file_path}' and set as the current graph.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"Error loading graph from '{file_path}': {e}")
