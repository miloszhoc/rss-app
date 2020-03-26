Aplikacja została postawiona w usłudze App Service z planem cenowym B1, które obsługuje manualne sklaowanie.    
Aplikacja podczas testów nie była skalowana.       
Do uruchomienia serwera została wykorzystana komenda `gunicorn --bind=0.0.0.0 --timeout 600 application:app  -k gevent --worker-connections 1000`

Z raportu wynika, że łącznie zostało wysłane 3600 requestów do 6 zasobów. 100% wysłanych requestów dotarło do serwera.   

Średni czas odpowiedzi był dość długi i wyniósł 22631.09 ms. Średnio na sekundę zostało dokonantych prawie 9 transakcji (8.82).    
Najbardziej problematyczna dla aplikacji okazała się metoda PUT, która aktualizuje link (średni czas odpowiedzi 37393.77 ms),   
następnie kolejno (od najdłuższego czasu odpowiedzi): 
- **metoda DELETE**, która usuwa url z bazy (średni czas odpowiedzi 35401.96 ms).
- **metoda GET**, która przygotowuje RSSy do wysyłki. Odczytuje RSSy z linków,    
wyciąga niezbędne informacje (tytuł, krótki opis i link) i łączy je w jeden obiekt (średni czas odpowiedzi 34226.24 ms)
- **metoda POST**, która dodaje url do bazy (średni czas odpowiedzi 28168.15ms)
- **metoda GET**, która pobiera listę linków (średni czas odpowiedzi 300.60 ms)
- **metoda GET**, która pobiera konkretny link (średni czas odpowiedzi 295.81 ms)


Średni czas oczekiwania na odpowiedź dla wszystkich requestow wyniósł 22626.57 ms.     
Dla poszczególnych metod wyniki prezentują się następująco: 
- dla **metody PUT**, która aktualizuje link - 37393.77 ms
- dla **metody DELETE**, która usuwa link - 35401.95 ms
- dla **metody GET**, która przygotowuje RSSy do wysyłki - 34199.19 ms
- dla **metody POST**, która dodaje url do bazy - 28168.142 ms
- dla **metody GET**, która pobiera listę linków - 300.59 ms
- dla **metody GET**, która pobiera konkretny link - 295.79 ms


Najprawdopodobniej niekorzystny wynik raportu orpócz powolnego algorytmu do łączenia RSS-ów wynika z wolnej bazy,    
która działa na prywatnym VPS o kiepskich parametrach. Niestety w chwili testów w nie było możliwości postawienia żadnej bazy w chmurze Microsoftu.

