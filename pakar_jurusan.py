import tkinter as tk
from tkinter import ttk, messagebox
from pyswip import Prolog

prolog = Prolog()
prolog.consult("pakar_jurusan.pl")

jurusan_list = []
minat_map = {}
index_jurusan = 0
index_minat = 0
current_jurusan = None
current_minat = None

def mulai_diagnosa():
    global jurusan_list, minat_map, index_jurusan, index_minat

    prolog.retractall("minat_pos(_)")
    prolog.retractall("minat_neg(_)")

    start_btn.configure(state=tk.DISABLED)
    yes_btn.configure(state=tk.NORMAL)
    no_btn.configure(state=tk.NORMAL)

    jurusan_list = [p["X"].decode() for p in prolog.query("jurusan(X)")]
    minat_map = {
        p: [g["X"] for g in prolog.query(f"minat(X, \"{p}\")")]
        for p in jurusan_list
    }
    index_jurusan = 0
    index_minat = -1
    pertanyaan_selanjutnya()

def pertanyaan_selanjutnya(ganti_jurusan=False):
    global index_jurusan, index_minat, current_jurusan, current_minat

    if ganti_jurusan:
        index_jurusan += 1
        index_minat = -1

    if index_jurusan >= len(jurusan_list):
        hasil_diagnosa(None)
        return

    current_jurusan = jurusan_list[index_jurusan]
    index_minat += 1

    if index_minat >= len(minat_map[current_jurusan]):
        hasil_diagnosa(current_jurusan)
        return

    current_minat = minat_map[current_jurusan][index_minat]

    if list(prolog.query(f"minat_pos({current_minat})")):
        pertanyaan_selanjutnya()
        return
    if list(prolog.query(f"minat_neg({current_minat})")):
        pertanyaan_selanjutnya(ganti_jurusan=True)
        return

    pert = list(prolog.query(f"pertanyaan({current_minat}, Q)"))[0]["Q"].decode()
    tampilkan_pertanyaan(pert)

def tampilkan_pertanyaan(teks):
    kotak_pertanyaan.configure(state=tk.NORMAL)
    kotak_pertanyaan.delete("1.0", tk.END)
    kotak_pertanyaan.insert(tk.END, teks)
    kotak_pertanyaan.configure(state=tk.DISABLED)

def jawaban(is_yes):
    if is_yes:
        prolog.assertz(f"minat_pos({current_minat})")
        pertanyaan_selanjutnya()
    else:
        prolog.assertz(f"minat_neg({current_minat})")
        pertanyaan_selanjutnya(ganti_jurusan=True)

def hasil_diagnosa(jurusan):
    if jurusan:
        messagebox.showinfo("Hasil Diagnosa", f"Sebaiknya anda memilih jurusan {jurusan}.")
    else:
        messagebox.showinfo("Hasil Diagnosa", "Tidak terdeteksi jurusan.")

    yes_btn.configure(state=tk.DISABLED)
    no_btn.configure(state=tk.DISABLED)
    start_btn.configure(state=tk.NORMAL)
    tampilkan_pertanyaan("")

root = tk.Tk()
root.title("Sistem Pakar Pemilihan Jurusan")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Aplikasi Konsultasi Pemilihan Jurusan", font=("Arial", 16)).grid(column=0, row=0, columnspan=3)

ttk.Label(mainframe, text="Pertanyaan:").grid(column=0, row=1, sticky=tk.W)
kotak_pertanyaan = tk.Text(mainframe, width=50, height=4, state=tk.DISABLED)
kotak_pertanyaan.grid(column=0, row=2, columnspan=3, pady=5)

yes_btn = ttk.Button(mainframe, text="Ya", state=tk.DISABLED, command=lambda: jawaban(True))
yes_btn.grid(column=1, row=3, sticky=(tk.W, tk.E))
no_btn = ttk.Button(mainframe, text="Tidak", state=tk.DISABLED, command=lambda: jawaban(False))
no_btn.grid(column=2, row=3, sticky=(tk.W, tk.E))

start_btn = ttk.Button(mainframe, text="Mulai Diagnosa", command=mulai_diagnosa)
start_btn.grid(column=1, row=4, columnspan=2, sticky=(tk.W, tk.E), pady=10)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()