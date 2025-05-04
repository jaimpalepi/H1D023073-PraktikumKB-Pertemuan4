% GEJALA PENYAKIT MALARIA
% DATABASE
:-dynamic gejala_pos/1.
:-dynamic gejala_neg/1.

% FAKTA & ATURAN
penyakit("Malaria Tertiana").
penyakit("Malaria Quartana").
penyakit("Malaria Tropika").
penyakit("Malaria Pernisiosa").

gejala(nyeri_otot, "Malaria Tertiana").
gejala(muntah, "Malaria Tertiana").
gejala(kejang, "Malaria Tertiana").
gejala(nyeri_otot, "Malaria Quartana").
gejala(menggigil, "Malaria Quartana").
gejala(tidak_enak_badan, "Malaria Quartana").
gejala(keringat_dingin, "Malaria Tropika").
gejala(sakit_kepala, "Malaria Tropika").
gejala(mimisan, "Malaria Tropika").
gejala(mual, "Malaria Tropika").
gejala(menggigil, "Malaria Pernisiosa").
gejala(tidak_enak_badan, "Malaria Pernisiosa").
gejala(demam, "Malaria Pernisiosa").
gejala(mimisan, "Malaria Pernisiosa").
gejala(mual, "Malaria Pernisiosa").

pertanyaan(nyeri_otot, Y) :-
    Y = "Apakah Anda merasa nyeri otot?".
pertanyaan(muntah, Y) :-
    Y = "Apakah Anda muntah-muntah?".
pertanyaan(kejang, Y) :-
    Y = "Apakah Anda mengalami kejang-kejang?".
pertanyaan(menggigil, Y) :-
    Y = "Apakah Anda sering menggigil?".
pertanyaan(tidak_enak_badan, Y) :-
    Y = "Apakah Anda merasa tidak enak badan?".
pertanyaan(keringat_dingin, Y) :-
    Y = "Apakah Anda mengalami keringat dingin?".
pertanyaan(sakit_kepala, Y) :-
    Y = "Apakah Anda sering sakit kepala?".
pertanyaan(mimisan, Y) :-
    Y = "Apakah Anda sering mimisan?".
pertanyaan(mual, Y) :-
    Y = "Apakah Anda merasa mual?".
pertanyaan(demam, Y) :-
    Y = "Apakah Anda demam?".
