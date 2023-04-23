# YassQueenDB 💁‍♀️👑🔍

!This readme is written by ChatGPT!

YassQueenDB is a graph database library that allows you to store, analyze, and search through your data in a graph format. By using the Universal Sentence Encoder, it provides an efficient and semantic approach to handle text data. 📚🧠🚀

## Benefits 😍

1. Semantic understanding of text data 📖
2. Efficient handling of relationships between data 💼
3. Easy-to-use graph manipulation functions 🛠️
4. Text summarization capabilities 📝
5. Keyword extraction for easy indexing and searching 🔎
6. Flexible graph creation and management 🌐

## Drawbacks 😔

1. Requires downloading and loading the Universal Sentence Encoder model 📥
2. Limited to text data only 🚫
3. Might be slow for very large datasets 🐌

## Features 🌟

### Graph Management 🗂️

* Create, select, and delete graphs 📁
* Add and delete nodes 📌
* Add and delete edges ↔️

### Text Analysis 📖

* Semantic search for nodes 🧐
* Summarize sections and paragraphs 📝
* Split paragraphs into sentences and create nodes from them 📚

### Data Manipulation 🧩

* Generate embeddings for text data 🔍
* Extract keywords from input data 🏷️
* Laplacian eigenmaps for dimensionality reduction 📉
* Save and load graphs to/from files 💾

## Usage 🛠️

```python
from yassqueendb import GraphDatabase

#Create a YassQueenDB instance

db = GraphDatabase()

# Load the sentence encoder

db.load_sentence_encoder()

# Create a graph

db.create_graph('example_graph')

# Add a node

db.add_node('This is a sample sentence.')

# Add an edge between nodes

db.add_edge('node1', 'node2', 'relationship_name')

# Search for a node

db.search_node('node1')

# Show the graph

db.show_graph()

# Save the graph to a file

db.save_graph_to_file('example_graph.pickle')

# Load the graph from a file

db.load_graph_from_file('example_graph.pickle')

# Summarize a section of text

section = "This is a section of text. It has multiple paragraphs."
section_summary = db.summarize_section(section)`
```

Get started with YassQueenDB and unleash the power of semantic graph databases! 🎉💃🕺
