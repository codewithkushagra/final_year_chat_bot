from __future__ import absolute_import, unicode_literals

import re
import uuid
import logging

from celery import shared_task
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

from apps.bot.utils.gemini import GeminiLLM


logger = logging.getLogger(__name__)


QDRANTDB_HOST = "localhost"
QDRANTDB_PORT = 6333


def chunk_text_by_sentences(text, max_chunk_size=512):
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) > max_chunk_size:
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk += (' ' if current_chunk else '') + sentence
    
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks


@shared_task()
def ingest_data(text):
    client = QdrantClient(host=QDRANTDB_HOST, port=QDRANTDB_PORT)
    chunks = chunk_text_by_sentences(text)
    points = []
    try:
        for i, chunk in enumerate(chunks):
            print(chunk)
            embedding = GeminiLLM.generate_embeddings(text=chunk)
            if embedding:
                point_id = str(uuid.uuid4())
                print(embedding)
                points.append(PointStruct(payload={"data": chunk}, vector=embedding, id=point_id))
        client.upsert(
            collection_name="zomato_vector",
            wait=True,
            points=points,
        )
    except Exception as e:
        logger.info(e)


def create_index(index_name, client, size=786, distance=Distance.DOT):
    client.create_collection(
        collection_name=index_name,
        vectors_config=VectorParams(size=size, distance=Distance.DOT),
    )

# search_result = client.search(
#     collection_name="zomato_vector", query_vector=embedding, limit=2
# )
