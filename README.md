# logfile
Celem zadania jest napisanie skryptu parsującego logi serwera Gunicorn.

Skrypt powinien posiadać następujące cechy:
Aplikacja konsolowa
Aplikacja używająca pythona 3.8 bez zewnętrznych zależności (do pisania testów można użyć Pytest)
Aplikacja na wejściu dostaje nazwę pliku zawierającego poprawny output serwera Gunicorn (co za tym idzie, aplikacja nie powinna przerwać swojego działania z nieobsłużonym błędem), jednak same logi pochodzą z journalctl, można założyć, że format journalctl się nie zmieni, format logów Gunicorn podany niżej.
Skrypt powinien umożliwić wypisanie statystyk dla danego przedziału czasowego (lub wszystkich):
Ilość zapytań
Średnia ilość zapytań na sekundę
Ilość poszczególnych kodów odpowiedzi serwera (200: 10, 301: 20, 500: 56 etc.)
Średnia wielkość wygenerowanej odpowiedzi (dla zapytań z kodem 2xx)

format logów Gunicorn (opis w dokumentacji):
%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s

Możliwe wektory zmiany (change vectors) na które można przygotować kod (konfigurowalność):
- inny format logów Gunicorn
- dodanie kolejnych statystyk
- zmiana formatu wyświetlania wyjścia

Przykładowe wywołanie:
python parser.py --from 20-11-2016_11-23-11 --to 21-11-2016_01-33 logfile.log
python parser.py --from 20-11-2016_11-23-11 logfile.log
python parser.py --to 21-11-2016_01-33 logfile.log
python parser.py logfile.log

Przykładowe wyjście:
requests: 5361
requests/sec: 3.5
responses: (200: 10, 301: 20, 500: 56)
avg size of 2xx responses: 4.32 Mb
