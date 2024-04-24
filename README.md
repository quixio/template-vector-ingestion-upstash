# Continuous Vector Ingestion using Quix and Upstash

This template shows you how to continuously ingest documents into a vector store using Apache Kafka. For simplicity, this use case is illustrated by streaming data from small CSV files that represent updates to a book catalog. The descriptive text from the catalog entries is then embedded and then ingested it into a vector store for semantic search. In a production scenario, you might use Change Data Capture (CDC) to ensure that the vector store is in sync with the book catalog database.

This template uses the following open source libraries:

* **[Quix Streams](https://github.com/quixio/quix-streams)** to produce data to, and consume data from, Apache Kafka.

* **[Upstash Vector Python SDK](https://github.com/upstash/vector-py)** to store the embeddings in the Upstash vector database.

The following screenshot illustrates the architecture of the resulting pipeline in Quix Cloud:
![Pipeline sscreenshot](https://github.com/quixio/template-vector-ingestion-upstash/assets/116729413/a3ade223-60fb-4352-84fb-775bbfb34d8a)

You can also try out a minimal version of this pipeline in a [standalone Jupyter notebook](./continuously_ingest_documents_into_upstash_vector_store_using_quix_and_kafka.ipynb
). 
* To run it Google Colab, click [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/quixio/template-vector-ingestion-upstash/blob/develop/continuously_ingest_documents_into_upstash_vector_store_using_quix_and_kafka.ipynb) .

## Trying it out
To try out the pipeline, first clone the vector ingestion template (for more information on how to clone a project template, see the article ["How to create a project from a template in Quix](https://quix.io/blog/how-to-create-a-project-from-a-template")). 

Before you clone the pipeline, you’ll also need to sign up for a free account with [Upstash](https://upstash.com/) (you can sign up with your GitHub or Google account). When you clone the project template in Quix, you’ll be asked for your Upstash credentials.

When running the project, you'll ingest content in two passes, 
* In the **first pass**, you'll add some initial entries to a "book-catalog" vector store via Kafka, then search the vector store (we've used the example query "book like star wars") to check that the data was ingested correctly.
* In the **second round** you'll go through the whole process again (albeit faster) with new data, and see how the matches change for the same search query .

### Run the first ingestion test

1. Press play on the first job (with the name that starts with “PT1…”)—hover your mouse over the “stopped” button to press play.<br><br>
   _This will ingest the first part of the same “sci-fi books” sample dataset that we used in the notebook._ <br><br>
2. In the [Upstash vector console](https://console.upstash.com/vector), open the data browser.<br><br>
3. Search for “book like star wars” — the top result should be “Dune”.<br><br>
   ![Upstash search1 screenshot](https://github.com/quixio/template-vector-ingestion-upstash/assets/116729413/e7351a9c-ff26-4986-a2c0-67a23f55abed)
   _We can assume it matched because the words in the description are semantically similar to the query: “planet" is semantically close to "star" and "struggles" is semantically close to "wars"._


### Run the second ingestion test

1. Press play on the second job (with the name that starts with “PT2…”)<br><br>
   _This will ingest the second part of the dataset with more relevant matches._ <br><br>
2. In the Upstash data browser, search for “books like star wars” again—the top result should now be “Old man’s war”, and the second result should be “Dune”.<br><br>
   ![Upstash search2 screenshot](https://github.com/quixio/template-vector-ingestion-upstash/assets/116729413/1c47d40b-2450-482a-a75e-653aeb4942f4)
   _We can assume that Dune has been knocked off the top spot because the new addition has a more semantically relevant description: the "term" war is almost a direct hit, and "interstellar" is probably semantically closer to the search term "star" than "planet"._
