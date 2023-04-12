# YassQueenDB

YassQueenDB is a simple graph database for storing and searching semantically related data. It is built using Python and leverages NetworkX, TensorFlow, and the Universal Sentence Encoder for generating node embeddings and performing semantic search.

## Features

YassQueenDB provides the following functionalities:

* Creating and managing multiple graph instances
* Adding nodes and edges (relationships) to a graph
* Generating embeddings for nodes using the Universal Sentence Encoder
* Searching for semantically related nodes based on a query
* Deleting nodes from a graph
* Saving and loading graphs to/from a file
* Laplacian Eigenmaps dimensionality reduction
* Showing graph structure and properties

Please refer to the inline comments in the code for more details on each method.

## Installation

Before using YassQueenDB, please ensure that you have the following Python packages installed:

* `networkx`
* `numpy`
* `scipy`
* `tensorflow`
* `tensorflow_hub`

You can install these packages using `pip`:

```bash
pip install networkx numpy scipy tensorflow tensorflow_hub
```

## Usage

To use YassQueenDB, simply import the `GraphDatabase` class:

```python
from YassQueenDB import GraphDatabase
```

Here's a quick example to get you started:

```python
# Instantiate the graph database
graph_db = GraphDatabase()


# Load sentence encoder

graph_db.load_sentence_encoder()

# Create a graph

graph_db.create_graph("my_graph")

# Add nodes with data

node_A = graph_db.add_node("This is a sample sentence for node A.")
node_B = graph_db.add_node("This is another sample sentence for node B.")

# Add relationship

graph_db.add_edge(node_A, node_B, "related")

# Show graph

graph_db.show_graph()

# Semantic search

results = graph_db.semantic_search("A sample sentence to search for.", top_k=1)
print(f"Semantic search results: {results}")
```

## Wanna see it in action?
https://colab.research.google.com/drive/13zRVd2zjxvyF0ZVQWS-hTSaFDNN8eyMH?usp=sharing
