% GEJALA PENYAKIT MALARIA
% DATABASE
% -- Menyimpan data apakah X memiliki gejala Y.
:- dynamic gejala/2.

% ATURAN
% -- Mengandung daftar gejala untuk beberapa jenis penyakit malaria,
% -- dengan predikat penyakit/2 (menerima dua parameter)
% -- yang berarti X mengidap penyakit Y.
% -- Predikat gejala/2 berarti X memiliki gejala Y.
penyakit(X, tertiana) :-
    gejala(X, nyeri_otot),
    gejala(X, muntah),
    gejala(X, kejang).

penyakit(X, quartana) :-
    gejala(X, nyeri_otot),
    gejala(X, menggigil),
    gejala(X, tidak_enak_badan).

penyakit(X, tropika) :-
    gejala(X, keringat_dingin),
    gejala(X, sakit_kepala),
    gejala(X, mimisan),
    gejala(X, mual).

penyakit(X, pernisiosa) :-
    gejala(X, menggigil),
    gejala(X, tidak_enak_badan),
    gejala(X, demam),
    gejala(X, mimisan),
    gejala(X, mual).
