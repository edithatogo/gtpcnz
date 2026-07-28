import functools
import time
from public.gtpcnz.models.primarycare_model.data.public_source_retrieval import load_public_source_retrieval_plans

start = time.time()
for _ in range(50):
    load_public_source_retrieval_plans()
print(f"Without cache: {time.time() - start:.4f}s")
