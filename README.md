# Diplomski rad
Ovdje se nalazi programski kod ostvarenog web sustava za ekstraktivno sažimanje teksta. Ostvareni sustav koristi model za ekstraktivno sažimanje čija je arhitektura preuzeta iz <a href="https://arxiv.org/abs/1906.04165">rada Dereka Millera</a>. Ekstraktivni sažetak sastoji se od odabranih rečenica koje najbolje opisuju ulazni tekst. Sažetak se stvara slijedom operacija: 
<ol>
  <li>Ulazni tekst se <b>dijeli na rečenice</b> korištenjem cjevovoda iz <a href="https://spacy.io/usage/spacy-101#pipelines">spaCy</a> programske knjižnice</li>
  <li>Za svaku rečenicu <b>računa se vektorska reprezentacija</b> korištenjem dubokog modela  <a href="https://arxiv.org/abs/1810.04805">BERT</a></li>
  <li>Vektorske reprezentacije rečenica ulaznog teksta se <b>grupiraju</b> algoritmom <a href="https://stanford.edu/~cpiech/cs221/handouts/kmeans.html">k-sredina</a></li>
  <li>Za izlazni sažetak se odabiru rečenice čije su <b>vektorske reprezentacije najbliže centrima</b> pojedinig grupa</li>
</ol>  

## Opis direktorija
Programski kod podijeljen je u dva direktorija. U direktoriju ***Summarization_system*** nalazi se programsko ostvarenje modela za ekstraktivno sažimanje teksta, a u direktoriju ***Web_app*** nalazi se ostvarenje web primjenskog sustava.
### Direktorij *Summarization_system*
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
### Direktorij *Web_app*
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
