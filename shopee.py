import threading
import time
import random

# Flag global untuk pembatalan (deferred cancellation)
cancel_flag = threading.Event()

# ==== THREAD A: Pencarian produk di kategori ====
def search_category(category, target):
    for i in range(1, 11):  # misalnya ada 10 halaman produk
        if cancel_flag.is_set():  # cek apakah perlu berhenti
            print(f"[{category:<10}]  ➔  Stop, sudah ada yang menemukan (deferred).")
            return

        # Simulasi waktu pencarian
        time.sleep(random.uniform(0.2, 0.5))

        # Simulasi probabilitas menemukan produk
        if random.random() < 0.2:
            print(f"[{category:<10}]  ✔  Produk '{target}' ditemukan di halaman {i}!")
            cancel_flag.set()  # kasih sinyal ke thread lain untuk stop
            return
        else:
            print(f"[{category:<10}]  •  Memeriksa halaman {i:2} ... belum ketemu.")

    print(f"[{category:<10}]  ✗  Produk '{target}' tidak ditemukan.")

# ==== THREAD B: Logging ====
def logger():
    while not cancel_flag.is_set():
        print("[Logger    ]  ⏳  Mencatat aktivitas pencarian...")
        time.sleep(0.7)
    print("[Logger    ]  🛑  Berhenti, pencarian selesai.")

# ==== THREAD C: Notifikasi ====
def notifier():
    cancel_flag.wait()  # tunggu sinyal produk ditemukan
    print("[Notifier  ]  📢  Notifikasi dikirim ke user: Produk ditemukan di Shopee!")

# ==== MAIN ====
if __name__ == "__main__":
    target_product = "Sepatu Nike"

    # Buat thread untuk kategori Shopee
    categories = ["Fashion", "Olahraga", "Promo"]
    search_threads = [threading.Thread(target=search_category, args=(cat, target_product)) for cat in categories]

    # Buat thread logger & notifier
    t_logger = threading.Thread(target=logger)
    t_notifier = threading.Thread(target=notifier)

    print("=== Mulai pencarian produk di Shopee ===\n")

    # Jalankan semua thread
    for t in search_threads: t.start()
    t_logger.start()
    t_notifier.start()

    # Tunggu semua thread selesai
    for t in search_threads: t.join()
    t_logger.join()
    t_notifier.join()

    print("\n=== Pencarian Shopee selesai ===")