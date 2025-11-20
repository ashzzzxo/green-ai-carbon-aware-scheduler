import time
import random


def main():
    print("[TRAIN] Starting dummy training...")
    for epoch in range(1, 6):
        time.sleep(1)  # simulate work
        print(f"[TRAIN] Epoch {epoch}/5 - loss={random.random():.3f}")
    print("[TRAIN] Training complete.")


if __name__ == "__main__":
    main()
