import tkinter as tk
from tkinter import ttk, messagebox
from pyswip import Prolog

# Inisialisasi Prolog dan konsultasi file pakar
prolog = Prolog()
prolog.consult("pakar_malaria_gui.pl")

# Variabel global untuk menyimpan data diagnosis
penyakit_list = []
gejala_map = {}
index_penyakit = 0
index_gejala = 0
current_penyakit = None
current_gejala = None

# Fungsi untuk memulai proses diagnosa
def mulai_diagnosa():
    global penyakit_list, gejala_map, index_penyakit, index_gejala

    # Bersihkan fakta gejala positif/negatif dari Prolog
    prolog.retractall("gejala_pos(_)")
    prolog.retractall("gejala_neg(_)")

    # Disable tombol Mulai, enable Ya/Tidak
    start_btn.configure(state=tk.DISABLED)
    yes_btn.configure(state=tk.NORMAL)
    no_btn.configure(state=tk.NORMAL)

    # Ambil daftar penyakit dan gejalanya
    penyakit_list = [p["X"].decode() for p in prolog.query("penyakit(X)")]
    gejala_map = {
        p: [g["X"] for g in prolog.query(f"gejala(X, \"{p}\")")]
        for p in penyakit_list
    }
    index_penyakit = 0
    index_gejala = -1
    pertanyaan_selanjutnya()

# Fungsi untuk menampilkan pertanyaan berikutnya
def pertanyaan_selanjutnya(ganti_penyakit=False):
    global index_penyakit, index_gejala, current_penyakit, current_gejala

    # Jika harus pindah ke penyakit berikutnya
    if ganti_penyakit:
        index_penyakit += 1
        index_gejala = -1

    # Jika daftar penyakit habis
    if index_penyakit >= len(penyakit_list):
        hasil_diagnosa(None)
        return

    current_penyakit = penyakit_list[index_penyakit]
    index_gejala += 1

    # Jika semua gejala penyakit sudah dicek
    if index_gejala >= len(gejala_map[current_penyakit]):
        hasil_diagnosa(current_penyakit)
        return

    current_gejala = gejala_map[current_penyakit][index_gejala]

    # Lewati jika fakta sudah ada
    if list(prolog.query(f"gejala_pos({current_gejala})")):
        pertanyaan_selanjutnya()
        return
    if list(prolog.query(f"gejala_neg({current_gejala})")):
        pertanyaan_selanjutnya(ganti_penyakit=True)
        return

    # Ambil teks pertanyaan dari file pakar
    pert = list(prolog.query(f"pertanyaan({current_gejala}, Q)"))[0]["Q"].decode()
    tampilkan_pertanyaan(pert)

# Fungsi untuk memperbarui kotak pertanyaan
def tampilkan_pertanyaan(teks):
    kotak_pertanyaan.configure(state=tk.NORMAL)
    kotak_pertanyaan.delete("1.0", tk.END)
    kotak_pertanyaan.insert(tk.END, teks)
    kotak_pertanyaan.configure(state=tk.DISABLED)

# Fungsi penanganan jawaban Ya/Tidak
def jawaban(is_yes):
    if is_yes:
        prolog.assertz(f"gejala_pos({current_gejala})")
        pertanyaan_selanjutnya()
    else:
        prolog.assertz(f"gejala_neg({current_gejala})")
        pertanyaan_selanjutnya(ganti_penyakit=True)

# Fungsi menampilkan hasil akhir diagnosa
def hasil_diagnosa(penyakit):
    if penyakit:
        messagebox.showinfo("Hasil Diagnosa", f"Anda terdeteksi {penyakit}.")
    else:
        messagebox.showinfo("Hasil Diagnosa", "Tidak terdeteksi penyakit.")

    # Reset tombol
    yes_btn.configure(state=tk.DISABLED)
    no_btn.configure(state=tk.DISABLED)
    start_btn.configure(state=tk.NORMAL)
    tampilkan_pertanyaan("")

# --- Bagian GUI ---
root = tk.Tk()
root.title("Sistem Pakar Diagnosis Penyakit Malaria")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Judul
ttk.Label(mainframe, text="Aplikasi Diagnosa Penyakit Malaria", font=("Arial", 16)).grid(column=0, row=0, columnspan=3)

# Kotak pertanyaan
ttk.Label(mainframe, text="Pertanyaan:").grid(column=0, row=1, sticky=tk.W)
kotak_pertanyaan = tk.Text(mainframe, width=50, height=4, state=tk.DISABLED)
kotak_pertanyaan.grid(column=0, row=2, columnspan=3, pady=5)

# Tombol Ya/Tidak
yes_btn = ttk.Button(mainframe, text="Ya", state=tk.DISABLED, command=lambda: jawaban(True))
yes_btn.grid(column=1, row=3, sticky=(tk.W, tk.E))
no_btn = ttk.Button(mainframe, text="Tidak", state=tk.DISABLED, command=lambda: jawaban(False))
no_btn.grid(column=2, row=3, sticky=(tk.W, tk.E))

# Tombol Mulai
start_btn = ttk.Button(mainframe, text="Mulai Diagnosa", command=mulai_diagnosa)
start_btn.grid(column=1, row=4, columnspan=2, sticky=(tk.W, tk.E), pady=10)

# Padding otomatis
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()