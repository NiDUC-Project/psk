## Phase Shift Keying

#### 1. Modulator (komputer A):
* wczytanie obrazu do programu python
* zamienienie obrazu na ciąg zer i jedynek
* utworzenie sygnału na podstawie ciągu tych zer i jedynek, odpowiednie zmodyfikowanie fazy
* przekazanie zmodyfikowanego sygnału do kanału transmisyjnego

#### 2. Kanał transmisyjny:
* Dodaje szum do naszego sygnału
* Szum musi dać się regulować, żeby potem sprawdzić jaki szum był krytyczny dla danego kluczenia

#### 3. Demodulator (komputer B):
* Odbiera sygnał jako zmodyfikowaną funkcję trygonometryczną z szumami
* Odczytanie przesunięć fazowych 
* Narysowanie diagramów konstelacji (na płaszczyźnie liczb zespolonych)
* Podczas odczytywania, klasyfikowanie pobranych punktów do odpowiednich grup na wykresie (tak żeby można było odczytać jakie znaki koduje dany punkt)
* Odtworzenie ciągu zer i jedynek
* Odtworzenie obrazu z ciągu zer i jedynek 
