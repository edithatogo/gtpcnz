import time
from models.primarycare_model.data.public_source_fetch import main

def run_benchmark():
    start = time.time()
    for _ in range(10): # Running 10 times to get a measurable time
        main(["--require-raw"])
    end = time.time()
    print(f"Benchmark took: {end - start:.4f} seconds")

if __name__ == "__main__":
    run_benchmark()
