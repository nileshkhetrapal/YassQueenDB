#The goal of this program is to allow the user to create a vector database for sentences.
#and then query it for the nearest neighbor of a given vector.
#The database is stored in a csv file in the same directory as the current working directory.
#The user can also add vectors to the database and delete vectors from the database.

# -*- coding: utf-8 -*-
"""Vector_DB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18BuiRsBgP--7lYZLuZj7dcpCAyBx3EVN
"""
import numpy as np
import pandas as pd
import textract
import tensorflow as tf
import tensorflow_hub as hub
import os
import argparse

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
embed = hub.load(module_url)



def create(tablename, documents):
    #This function creates a vector database for the given documents.
    text_data = get_text(documents)
    for text in text_data:
        print(text + "is being added")
        #Generate embeddings for the text
        embeddings = embed(text)
        #Store the embeddings in a Pandas DataFrame
        
    embeddings = embed(text_data)
    #Store the embeddings in a Pandas DataFrame
    df = pd.DataFrame(embeddings.numpy())
    #Set the column names to be more descriptive
    df.columns = ["vector_{}".format(i) for i in range(df.shape[1])]
    #Add a column to store the original text
    df["text"] = text_data
    print(tablename + "is being created")
    #Save the DataFrame to disk
    df.to_csv(tablename, index=False)
    return tablename

def get_text(documents):
    #This function returns a list of the text from the documents.
    text_data = []
    for document in documents:
        print("is being extracted")
        #Get all the sentences from the document
        sentences = textract.process(document).decode("utf-8").split(".")
        #Remove empty sentences
        sentences = [sentence for sentence in sentences if sentence != ""]
        text_data.append(sentences)
    return text_data

def update(tablename, documents):
    #This function updates the vector database with the given documents.
    #Load the vector database
    df = pd.read_csv(tablename)
    #Get the text from the documents
    text_data = get_text(documents)
    for text in text_data:
        print(text + "is being added")
        #Generate embeddings for the text
        embeddings = embed(text)
        #Store the embeddings in a Pandas DataFrame
    #print to commandline
    print(text_data + "is being added")
    #Generate embeddings for the text
    embeddings = embed(text_data)
    #Store the embeddings in a Pandas DataFrame
    new_df = pd.DataFrame(embeddings.numpy())
    #Set the column names to be more descriptive
    new_df.columns = ["vector_{}".format(i) for i in range(new_df.shape[1])]
    #Add a column to store the original text
    new_df["text"] = text_data
    #Append the new DataFrame to the old one
    df = df.append(new_df, ignore_index=True)
    #Save the DataFrame to disk
    df.to_csv(tablename, index=False)
    return tablename

def delete(tablename, query):
    print("delete")
    #This function deletes the vector from the database that is closest to the query.
    #Load the vector database
    df = pd.read_csv(tablename)
    #Generate an embedding for the query
    query_vector = embed([query]).numpy()[0]
    #Calculate the cosine similarity between the query vector and all vectors in the database
    cosine_similarities = np.dot(df.iloc[:,:-1], query_vector) / np.linalg.norm(df.iloc[:,:-1], axis=1) / np.linalg.norm(query_vector)
    #Sort the cosine similarities in descending order
    sorted_similarities = cosine_similarities.argsort()[::-1]
    print(sorted_similarities[0] + "is being deleted")
    #Delete the most similar sentence
    df = df.drop(sorted_similarities[0])
    #Save the DataFrame to disk
    df.to_csv(tablename, index=False)
    return tablename




def search(tablename, query):
    #This function returns the nearest neighbor of the query.
    #Load the vector database
    df = pd.read_csv(tablename)
    #Generate an embedding for the query
    query_vector = embed([query]).numpy()[0]
    #Calculate the cosine similarity between the query vector and all vectors in the database
    cosine_similarities = np.dot(df.iloc[:,:-1], query_vector) / np.linalg.norm(df.iloc[:,:-1], axis=1) / np.linalg.norm(query_vector)
    #Sort the cosine similarities in descending order
    sorted_similarities = cosine_similarities.argsort()[::-1]
    #Return the text of the most similar sentence
    return df.iloc[sorted_similarities[0]]["text"]

def main():
    #Parse the command line arguments
    parser = argparse.ArgumentParser(description="Create, update, and query a vector database.")
    parser.add_argument("command", help="The command to run. Either 'create', 'update', or 'search'.")
    parser.add_argument("tablename", help="The name of the vector database file.")
    parser.add_argument("--documents", nargs="+", help="The documents to add to the vector database.")
    parser.add_argument("--query", help="The query to search for in the vector database.")
    args = parser.parse_args()
    #Run the appropriate function
    if args.command == "create":    
        create(args.tablename, args.documents)
    elif args.command == "update":
        update(args.tablename, args.documents)
    elif args.command == "search":
        print(search(args.tablename, args.query))
    elif args.command == "delete":
        delete(args.tablename, args.query)
    else:
        print("Command not recognized.")

if __name__ == "__main__":
    main()
    