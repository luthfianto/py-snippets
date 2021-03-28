import ast
import os
import konstanta
import gensim
import pandas as pd
from gensim.models.doc2vec import TaggedDocument

try:
    os.makedirs('artifacts')
except OSError as e:
    pass

docs = []
for row in df3.itertuples():
    docs.append(TaggedDocument(words=row.tags, tags=[row.id]))

model = gensim.models.Doc2Vec(
    workers=4, epochs=50
)
model.build_vocab(docs)

print("Start training process...")
model.train(docs, total_examples=model.corpus_count, epochs=model.epochs)

model.save(konstanta.MODEL_PATH)
from gensim.similarities.annoy import AnnoyIndexer
annoy_index = AnnoyIndexer(model, 100)
annoy_index.save(konstanta.ANNOY_IDX)
