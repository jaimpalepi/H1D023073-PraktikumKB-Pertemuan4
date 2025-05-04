% GEJALA PENYAKIT MALARIA

% DATABASE
% -- Menyimpan data apakah gejala X positif atau negatif.
 :- dynamic gejala_pos/1.
 :- dynamic gejala_neg/1.

% ATURAN
% -- Predikat pertanyaan/1 untuk menanyakan pertanyaan terkait gejala X.
pertanyaan(nyeri_otot) :-
    write("Apakah anda merasa nyeri otot?").

pertanyaan(muntah) :-
    write("Apakah Anda muntah-muntah?").

pertanyaan(kejang) :-
    write("Apakah Anda mengalami kejang-kejang?").

pertanyaan(menggigil) :-
    write("Apakah Anda sering menggigil?").

pertanyaan(tidak_enak_badan) :-
    write("Apakah Anda merasa tidak enak badan?").

pertanyaan(keringat_dingin) :-
    write("Apakah Anda mengalami keringat dingin?").

pertanyaan(mimisan) :-
    write("Apakah Anda sering mimisan?").

pertanyaan(mual):-
    write("Apakah Anda merasa mual?").

pertanyaan(demam) :-
    write("Apakah Anda demam?").
% -- Predikat diagnosa/1 digunakan untuk menanyakan dan menyimpan status
% gejala X.
diagnosa(G) :-
    pertanyaan(G),
    writeln(" (y/t)"),
    read(Jawaban),
    Jawaban == y,
    assertz(gejala_pos(G)).
diagnosa(G) :-
    assertz(gejala_neg(G)),
    fail.
%-- Predikat gejala/1 dipanggil untuk memerika status gejala dari
% database
% -- atau menanyakan user terkait gejala tersebut.
gejala(G) :-
    gejala_pos(G), !.

gejala(G) :-
    gejala_neg(G), !,
    fail.
gejala(G) :-
    diagnosa(G).

% -- Mengandung daftar gejala untuk beberapa jenis penyakit malaria,
% -- dengan predikat penyakit/1 (menerima satu parameter)
% -- yang berarti mengidap penyakit X.
penyakit(tertiana) :-
    gejala(nyeri_otot),
    gejala(muntah),
    gejala(kejang),
    terdeteksi("Malaria Tertiana").

penyakit(quartana) :-
    gejala(nyeri_otot),
    gejala(menggigil),
    gejala(tidak_enak_badan),
    terdeteksi("Malaria Quartana").

penyakit(tropika) :-
    gejala(keringat_dingin),
    gejala(sakit_kepala),
    gejala(mimisan),
    gejala(mual),
    terdeteksi("Malaria Tropika").

penyakit(pernisiosa) :-
    gejala(menggigil),
    gejala(tidak_enak_badan),
    gejala(demam),
    gejala(mimisan),
    gejala(mual),
    terdeteksi("Malaria Pernisiosa").

penyakit(_) :-
    writeln("Tidak terdeteksi penyakit.").

% -- Predikat terdeteksi/1 dipanggil untuk mencetak penyakit.
terdeteksi(P) :-
    write("Anda terdeteksi penyakit "),
    writeln(P).

% -- Predikat clear_db/0 untuk membersihkan database gejala.
clear_db :-
    retractall(gejala_pos(_)),
    retractall(gejala_neg(_)).

% -- Predikat main/0 sebagai main loop sistem pakar.
main :-
    write('\33\[2J'), % Clear window
    writeln("DIAGNOSA PENYAKIT THT"),
    penyakit(_),
    clear_db,
    writeln("INGIN MENGULANG?"),
    read(Jawaban), !,
    Jawaban == y,
    main.
