import tensorflow as tf
import tensorflow.keras.preprocessing.text as kpt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding
import networkx as nx
import numpy as np

import tensorflow_hub as hub
embed = hub.KerasLayer("https://tfhub.dev/google/universal-sentence-encoder/4")

class SentenceGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_sentence(self, sentence_id, sentence_text, sentence_vector):
        self.graph.add_node(sentence_id, text=sentence_text, vector=sentence_vector)

    def remove_sentence(self, sentence_id):
        self.graph.remove_node(sentence_id)

    def update_sentence(self, sentence_id, new_text, new_vector):
        self.graph.nodes[sentence_id]['text'] = new_text
        self.graph.nodes[sentence_id]['vector'] = new_vector

    def delete_graph(self):
        self.graph.clear()

    def query(self, query_vector, top_k=5):
        sentences_vectors = np.array([data['vector'] for _, data in self.graph.nodes(data=True)])
        similarity_scores = np.dot(sentences_vectors, query_vector)
        top_k_indices = np.argsort(similarity_scores)[-top_k:][::-1]
        top_k_sentence_ids = [list(self.graph.nodes())[index] for index in top_k_indices]
        return [(self.graph.nodes[id]['text'], similarity_scores[index]) for id, index in zip(top_k_sentence_ids, top_k_indices)]

sentence_graph = SentenceGraph()

sentences = ["This is a sample sentence. Cats", "Another example sentence. Dog"]
sentence_ids = range(len(sentences))
sentence_vectors = embed(sentences).numpy()

for sentence_id, sentence_text, sentence_vector in zip(sentence_ids, sentences, sentence_vectors):
    sentence_graph.add_sentence(sentence_id, sentence_text, sentence_vector)

query_sentence = "Bark"
query_vector = embed([query_sentence]).numpy()[0]
top_k_results = sentence_graph.query(query_vector, top_k=1)
print(top_k_results)

sentence_graph.update_sentence(0, "Updated sentence.", embed(["Updated sentence."]).numpy()[0])
sentence_graph.remove_sentence(1)

sentence_graph.delete_graph()
