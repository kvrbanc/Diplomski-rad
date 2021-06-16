# Diplomski rad
Ovdje se nalazi programski kod ostvarenog web sustava za ekstraktivno sažimanje teksta. Ostvareni sustav koristi model za ekstraktivno sažimanje čija je arhitektura preuzeta iz <a href="https://arxiv.org/abs/1906.04165">rada Dereka Millera</a>. Ekstraktivni sažetak sastoji se od odabranih rečenica koje najbolje opisuju ulazni tekst. Sažetak se stvara slijedom operacija: 
<ol>
  <li>Ulazni tekst se <b>dijeli na rečenice</b> korištenjem cjevovoda iz <a href="https://spacy.io/usage/spacy-101#pipelines">spaCy</a> programske knjižnice</li>
  <li>Za svaku rečenicu <b>računa se vektorska reprezentacija</b> korištenjem dubokog modela  <a href="https://arxiv.org/abs/1810.04805">BERT</a></li>
  <li>Vektorske reprezentacije rečenica ulaznog teksta se <b>grupiraju</b> algoritmom <a href="https://stanford.edu/~cpiech/cs221/handouts/kmeans.html">k-sredina</a></li>
  <li>Za izlazni sažetak se odabiru rečenice čije su <b>vektorske reprezentacije najbliže centrima</b> pojedinih grupa</li>
</ol>  

## Opis direktorija
Programski kod podijeljen je u dva direktorija. U direktoriju ***Summarization_system*** nalazi se programsko ostvarenje modela za ekstraktivno sažimanje teksta, a u direktoriju ***Web_app*** nalazi se ostvarenje web primjenskog sustava.
### Direktorij *Summarization_system*
U ovom direktoriju nalazi se programski kod koji ostvaruje funkcionalnost modela za ekstraktivno sažimanje teksta. Direktorij sadrži datoteku ***requirements.txt*** i potdirektorij ***bertsummarizer***.
<pre>
\---Summarization_system
  |   requirements.txt 
  \---bertsummarizer
    |   bert_wrapper.py
    |   kmeans_wrapper.py
    |   sentence_separator.py
    |   summarizer_model.py
    |   testing.py
    |   __init__.py
</pre>
Potdirektorij ***bertsummarizer*** sadrži datoteke programskog jezika *Python* kojima je ostvaren model za sažimanje teksta. Pritom datoteka ***\_\_init\_\_.py*** služi kako bi se direktorij označio kao paket programskog jezika *Python*, a datoteka ***testing.py*** služi za ispitivanje modela. Ostale datoteke koje uključuju ***bert_wrapper.py***, ***kmeans_wrapper.py***, ***sentence_separator.py*** i ***summarizer_model.py*** programski ostvaruju model.</br></br>
Datoteka ***requirements.txt*** sadrži popis i verzije *Python* paketa koje je potrebno instalirati na računalo kako bi se mogla koristiti funkcionalnost modela za ekstraktivno sažimanje teksta. Preporučeno je korištenje <a href="https://docs.python.org/3/library/venv.html">Python virtualnog okruženja</a> pri intalaciji potrebnih *Python* paketa. 
### Direktorij *Web_app*
U ovom direktoriju nalazi se programski kod koji ostvaruje web primjenski sustav. Web sustav razvijen je pomoću razvojnog okvira <a href="https://www.djangoproject.com/">Django</a>. Direktorij sadrži datoteku ***requirements.txt*** i potdirektorij ***application_source***.
<pre>
\---Summarization_system
  |   requirements.txt 
  \---application_source
    |   db.sqlite3
    |   manage.py
    \---summarizer
      | ...
    \---summarizerApp
      | ...
</pre>
Datoteka ***requirements.txt*** sadrži *Python* pakete i njihove verzije koje je potrebno instalirati na računalo kako bi se mogao koristiti web primjenski sustav. Ovdje je također preporučeno korištenje <a href="https://docs.python.org/3/library/venv.html">Python virtualnog okruženja</a>.</br></br>
Potdirektorij ***application_source*** sadrži programski kod Django web sustava. Datoteka ***db.sqlite3*** predstavlja *SQLite* bazu podataka, a datoteka ***manage.py*** služi izvođenju administrativnih zadataka nad web sustavom korištenjem naredbene linije.  
Potdirektorij ***summarizerApp*** predstavlja glavnu komponentu ostvarenog web sustava i sadrži datoteke za izmjenu *postavki sustava* i definiranje osnovne *URL sheme* sustava.</br>
Potdirektorij ***summarizer*** predstavlja komponentu web sustava koja ostvaruje njegove funkcionalnosti. Ovdje se nalaze sve *HTML*, *CSS* i *JavaScript* datoteke kojima su ostvarene web stranice sustava. Također, ovdje se nalaze datoteke kojima se definira *URL shema*, *poslužuju web stranice* i *poslužuju programski zahtjevi* za ekstraktivnim sažimanjem teksta. Pri posluživanju zahtjeva za sažimanjem teksta se pritom koristi ostvareni *model za ekstraktivno sažimanje*. Model se koristi kao paket programskog jezika *Python*. Kako bi se model mogao koristiti kao instalirani paket, direktorij ***bertsummarizer*** s datotekama koje ostvaruju model za ekstraktivno sažimanje teksta je ugrađen u korišteno *Python virtualno okruženje*.
