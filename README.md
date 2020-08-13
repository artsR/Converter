# Convert-GGnet-to-HM2

Program pobiera kod html i konwertuje znalezione tam dane do odpowiedniej formy zapisując je w pliku txt.

Krótki opis plików:
- download.py:
Założeniem programu jest emitowanie pracy użytkownika komputera dlatego oparłem program na bibliotece pyautogui.
Jego zadaniem jest klikanie odpowiednich elementów strony aby otworzyć jego podstronę, która następnie jest zapisywana na dysku.

- import - hands.py
Program otwiera zapisane poprzednio podstony i przeszukując kod HTML konwertuje znajdujące się tam dane do pliku tekstowego.
Na tym etapie wyłapywany jest również potencjalny błąd spowodowany zapisaniem nieodpowiedniej podstrony przez poprzedni program i umieszczenie w pliku tekstowych errors.txt informacji o numerze podstrony.

- download_errors.py
Program sprawdza, czy nie ma brakujących numerów podstron (np. 1,3,4 - program wykryje, że nie ma drugiej podstrony). I dodaje brakujące numery do pliku errors.txt
Następnie pobiera jeszcze raz te podstrony, których numery zostały umieszczone w pliku errors.txt. (Pobieranie odbywa się na tej samej zasadzie co w pliku download.py

- import - errors.py
Działanie jest analogiczne do działania pliku 'import - hands.py' jednak konwertowane są tylko te podstrony, które nie zostały skonwertowane poprzednim razem.
