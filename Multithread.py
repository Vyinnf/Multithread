import threading
import time
import random

# ==== GLOBAL FLAG untuk pembatalan (dipakai di mode deferred) ====
cancel_flag = threading.Event()

# ==== THREAD A: Pencarian data ====
def search_data(data, target):
    for i, val in enumerate(data):
        # Cek pembatalan secara DEFERRED
        if cancel_flag.is_set():
            print("[Search] Thread berhenti (deferred).")
            return

        if val == target:
            print(f"[Search] Target {target} ditemukan di index {i}")
            # kalau ketemu, aktifkan flag pembatalan (agar thread lain tahu)
            cancel_flag.set()
            return

        # Simulasi kerja berat
        if i % 50000 == 0:
            print(f"[Search] Sedang memeriksa index {i}")
            time.sleep(0.001)

    print("[Search] Target tidak ditemukan.")

# ==== THREAD B: Logging ====
def logger():
    while not cancel_flag.is_set():
        print("[Logger] Mencatat aktivitas...")
        time.sleep(0.5)
    print("[Logger] Thread berhenti.")

# ==== THREAD C: Notifikasi ====
def notifier():
    # Tunggu sampai ada flag cancel (artinya target sudah ditemukan)
    cancel_flag.wait()
    print("[Notifier] Notifikasi dikirim: Target ditemukan!")

# ==== MAIN PROGRAM ====
if __name__ == "__main__":
    # Buat array besar
    data = [random.randint(0, 1000000) for _ in range(200000)]
    target = data[123456]  # sengaja sisipkan target

    # Buat thread-thread
    t1 = threading.Thread(target=search_data, args=(data, target))
    t2 = threading.Thread(target=logger)
    t3 = threading.Thread(target=notifier)

    # Mulai semua thread
    t1.start()
    t2.start()
    t3.start()

    # Tunggu semua thread selesai
    t1.join()
    t2.join()
    t3.join()

    print("Program selesai.")
