from __future__ import absolute_import, unicode_literals

import re
import uuid
import logging

from celery import shared_task
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

from apps.bot.utils.gemini import GeminiLLM
from apps.ingest.models import Ingest, IngestStatus

logger = logging.getLogger(__name__)


QDRANTDB_HOST = "localhost"
QDRANTDB_PORT = 6333


def chunk_text_by_sentences(text, max_chunk_size=512):
    sentences = re.split(r"(?<=[.!?]) +", text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) > max_chunk_size:
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk += (" " if current_chunk else "") + sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def embed_and_insert(text, ingest_instance):
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
                points.append(
                    PointStruct(payload={"data": chunk}, vector=embedding, id=point_id)
                )
        client.upsert(
            collection_name="zomato_vector",
            wait=True,
            points=points,
        )
        ingest_instance.status = IngestStatus.COMPLETE
        ingest_instance.save()
    except Exception as e:
        ingest_instance.status = IngestStatus.FAILED
        ingest_instance.save()
        logger.info(e)


@shared_task()
def ingest_data(ingest_id):
    try:
        ingest_instance = Ingest.objects.get(id=ingest_id)
        ingest_instance.status = IngestStatus.PROCESSING
        ingest_instance.save()
        text = ingest_instance.text_data
        file = ingest_instance.file
        if text:
            embed_and_insert(text=text, ingest_instance=ingest_instance)

        if file:
            pass
    except Ingest.DoesNotExist:
        looger.error(f"Ingest with ingest id: {ingest_id} does not exist.")
    except Exception as e:
        ingest_instance.status = IngestStatus.FAILED
        ingest_instance.save()
        logger.error(f"Error processing ingest data.")


def create_index(index_name, size=768, distance=Distance.DOT):
    client = QdrantClient(host=QDRANTDB_HOST, port=QDRANTDB_PORT)
    client.create_collection(
        collection_name=index_name,
        vectors_config=VectorParams(size=size, distance=Distance.DOT),
    )


# search_result = client.search(
#     collection_name="zomato_vector", query_vector=embedding, limit=2
# )
