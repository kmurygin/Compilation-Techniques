# KacperScript
## Dokumentacja końcowa

Celem projektu było stworzenie języka, oferującego podstawowe własności
języków programowania wraz z wbudowanym typem słownika.
Dostępne operacje na słowniku:
- dodawanie elementów
- usuwanie elementów
- wyszukiwanie elementów według klucza
- iterowanie po elementach zgodnie z zadaną kolejnością
- wykonanie na słowniku zapytań w stylu LINQ

## Sposób uruchomienia interpreter:
Do uruchomienia programu napisanego w KacperScript wymagany jest zainstalowany Python.
Uruchamiamy poprzez komendę:
````
./main.py <sciezka_do_programu>
````

Przykładowy kod
```
function List<string> linq_test(){
    Dict<int, string> ludzie = {19: "Kacper", 7: "Klara", 21: "Steve"};
    List<string> adults = from Pair<int, string> para in ludzie where para.first() > 18 select para.second() orderby para.first();

    return adults;
}

function int main(){
    List<int> lista = [1, 2, 3, 4];
    for (int a in lista) {
        print(a);
    };
    print(linq_test());
    return 0;
}
```
Ten kod definiuje dwie funkcje: `linq_test()` i `main()`, w języku KacperScript.

### Funkcja `linq_test()`:
- Zwraca listę łańcuchów znaków.
- Tworzy słownik `ludzie` zawierający informacje o ludziach (klucz: wiek, wartość: imię).
- Tworzy listę `adults` zawierającą imiona dorosłych osób (wiek > 18), posortowane wg wieku.
- Zwraca listę `adults`.

### Funkcja `main()`:
- Zwraca liczbę całkowitą.
- Tworzy listę `lista` z czterema liczbami całkowitymi.
- Iteruje przez elementy listy `lista`, wypisując każdy na ekran.
- Wypisuje wynik funkcji `linq_test()`.
- Zwraca wartość `0`.

## Moduły projektu

### Reader
Moduł **Reader** jest odpowiedzialny za interakcję z zewnętrznym źródłem danych, takim jak plik tekstowy lub strumień wejściowy. Jego głównym zadaniem jest odczytywanie tekstu źródłowego programu z tego źródła w sposób kontrolowany. Może to obejmować odczytywanie tekstu po jednym znaku lub linii na raz, w zależności od potrzeb analizatorów leksykalnych i parserów. Moduł **Reader** zapewnia interfejs do odczytu i nawigacji po tekście źródłowym, a także obsługę zdarzeń, takich jak osiągnięcie końca pliku lub napotkanie błędu podczas odczytu.

### Lexer
Lexer jest często nazywany **analizatorem leksykalnym**. Jego głównym zadaniem jest przekształcenie sekwencji znaków z tekstu źródłowego na strumień tokenów, które reprezentują najmniejsze jednostki leksykalne języka programowania, takie jak słowa kluczowe, identyfikatory, liczby, operatory, itp. Moduł **Lexer** wykonuje analizę leksykalną, rozpoznając i klasyfikując różne typy tokenów zgodnie z regułami gramatyki języka. Tokeny te są później przekazywane do **analizatora składniowego** (parsera) w celu dalszej analizy i przetwarzania.

### Parser
Parser jest **analizatorem składniowym**, który przekształca strumień tokenów wygenerowanych przez lekser na strukturę drzewa składniowego. Drzewo składniowe odzwierciedla hierarchię składniową programu, zgodnie z regułami gramatyki języka programowania. **Parser** analizuje sekwencję tokenów, sprawdzając ich kolejność i relacje, aby zbudować poprawną strukturę drzewa składniowego. W przypadku błędów składniowych parser może zgłosić wyjątek lub przeprowadzić próbę naprawy błędów.

### Interpreter
Interpreter wykonuje kod programu, który został przetworzony przez **analizator składniowy**. Jest odpowiedzialny za interpretację struktury drzewa składniowego i wykonanie odpowiednich działań zgodnie z instrukcjami zawartymi w programie. Interpreter przechodzi przez każdy element drzewa składniowego, wykonując operacje takie jak przypisywanie wartości do zmiennych, wywoływanie funkcji, kontrola przepływu, operacje arytmetyczne, itp. Wyniki operacji są zazwyczaj przechowywane w pamięci i mogą być wykorzystywane w kolejnych krokach wykonania programu.

## Wymagania funkcjonalne i niefunkcjonalne:
1. Program musi zawierać funkcję main ze zwracanym typem int
2. Każda linia kodu kończy się średnikiem- „;”
3. Język pozwala na pisanie komentarzy
4. Można definiować własne funkcje, wywoływać je rekurencyjnie

## Obsługa podstawowych typów danych liczbowych:
1. Rodzaje danych liczbowych:
- typ całkowitoliczbowy ze znakiem int
- typ zmiennoprzecinkowy float
2. Operacje matematyczne:
- Mnożenie *
- Dzielenie /
- Dodawanie +
- Odejmowanie -
- Priorytet wykonywania operacji matematycznychstandardowy:
1. wykonywanie działań wewnątrz nawiasów
2. mnożenie i dzielenie
3. dodawanie i odejmowanie 

## Obsługa typu znakowego:
1. Typ znakowy string
2. Dozwolone operacje- konkatenacja
3. String może zawierać dowolne znaki, w tym:
- Wyróżnik stringa- cudzysłów
- Znak nowej linii
- Znak tabulacji

## Konwersja typów
W języku będą dostępne dwa rodzaje konwersji typów:
- z float na float
- z float na int.
- z int/float na string

Pierwszy przypadek jest prostszy, do liczby całkowitej zostaje dodana
część ułamkowa równa 0. W drugim przypadku zaś, część ułamkowa
zostaje wycięta, pozostaje jedynie część całkowita.
```
int x = 10;
float y = get_float(x); # y = 10.0
float a = 5.9;
int b = get_int(a); # b = 5
string c = get_string(b)
```
W przypadku innych konwersji- niedozwolonych np. próba konwersji
stringa na int, zostanie zgłoszony wyjątek.

## Typ słownika Dict
1. Stworzenie nowej zmiennej o typie Dict- pusty słownik bez
zawartości:
- Dict<typ_klucza, typ_wartosci> nazwa_zmiennej;
2. Konstruktor słownika ze startową zawartością:
- Dict<typ_klucza, typ_wartosci> nazwa_zm= {klucz: wartosc};
Przykłady:
```
Dict<string, int> dict_1;
Dict<string, int> dict_data = {“dzien”: 1, “miesiac”: 1, “rok”: 2024};
```
3. Dodawanie elementu do słownika:
- nazwa_zmiennej.add(klucz, wartosc);
```
dict_1("rok", 2024);
```
4. Usuwanie elementu ze słownika – usuwany element o podanym
kluczu:
- nazwa_zmiennej.delete(klucz);
```
dict_1.delete(“rok”);
```
5. Wyszukiwanie elementu według klucza:
- nazwa_zmiennej.get(wartosc_klucza);
```
dict_data.get(“rok”);
```
6. Sprawdzanie, czy dany klucz znajduje się w słowniku:
- nazwa_zmiennej.contains(wartosc_klucza);
```
dict_data.contains(“dzien”); #zwróci true
dict_data.contains(“naleśniki”); #zwróci false
``` 
7. Wykonywanie zapytań w stylu LINQ- SELECT WHERE FROM:
```
Dict<string, int> dictionary;
dictionary(“Kamil”, 20);
dictionary(“Marta”, 17);
List<Pair<string, int>> rezultat = from para in dictionary
where para.second > 18
select pair;
```

## Typ List:
1. Konstruktor:
- List<typ> nazwa_zmiennej;
- List<typ> nazwa_zmiennej = [1, 2, 3];
2. Dostęp do elementów listy za pomocą indeksu- metoda at:
Jeżeli nie ma elementu o danym indeksie, zostaje zgłoszony błąd.
```
nazwa_zmiennej.at(indeks)
```
3. Dodanie nowego elementu do listy- metoda append:
Jeżeli dodawany element nie zgadza się z typem
przechowywanym w liście, zostaje zgłoszony błąd.
```
nazwa_zmiennej.append(wartosc)
```
4. Usunięcie elementu z listy- metoda remove:
Usuwa pierwsze wystąpienie danego elementu w liście, jeżeli
element nie istnieje w liście zostaje zgłoszony błąd.
```
nazwa_zmiennej.remove(wartosc)
```
Przykłady:
```
List<string> imiona;
imiona.append(“Kasia”);
imiona.append(“Basia”);
imiona.append(“Kamil”);
print(imiona.at(0)) //wypisana zostanie imie “Kasia”
imiona.remove(“Kamil”)
```
## Typ Pair:
1. Konstruktor:
```
Pair<typ_1, typ_2> nazwa_zmiennej;
Pair<typ_1, typ_2> nazwa_zmiennej = (1, 2);
```
2. Dostęp do elementów w parze:
```
nazwa_zmiennej.first() -> zwraca pierwszy element pary
nazwa_zmiennej.second() -> zwraca drugi element pary
```
Przykłady:
```
Pair<string, string> para_1;
Pair<string, string> para_2 = (“Kamil”, “Basia”);
pair_1.first() = “Antonina”;
pair_1.second() = “Grzegorz”;
string imie_21 = pair_2.first; #zmiennej imie_21 zostanie przypisana
# wartość “Kamil”
string imie_22 = pair_2.second; #zmiennej imie_22 zostanie przypisana
# wartość “Basia”
```
## Obsługa komentarzy:
1. Cała linia począwszy od znaku “#”:
```
# komentarz 1
# komentarz 2
# komentarz 3
```
## Zmienne- przypisywanie do nich wartości i odczytywanie ich:
1. Semantyka obsługi zmiennych:
- Typowanie statyczne
- Typowanie silne
- Zmienne są mutowalne
2. Zakresy widoczności zmiennych
- lokalny zakres
```
function void funkcja_1() {
int a = 10;
print(a)
}
```
Zmienna zdefiniowana wewnątrz ciała funkcji, jest dostępna tylko
w tym bloku.
- Zakres globalny
```
int a = 10;
function int main(){
    print(a);
}
```
## Instrukcja warunkowa if
```
int zmienna = 4;
if (zmienna == 4) {
print(“Tak’);
}
else {
print(“Nie”);
}
if (zmienna < 0) { print(“Ujemna”); }
else if (zmienna == 0) { print(“Zero”); }
else if (zmienna > 0) { print(“Dodatnia”); }
if (zmienna <= 0) { print(“Niedodatnia”); }
if (zmienna >= 0) { print(“Nieujemna”); }
```
## Instrukcja pętli for
Pętla for w moim języku będzie podobna składnią do innych języków
programowania.
```
for ( typ_zmiennej zmienna : iterowalna_zmienna) {
    //blok instrukcji
    //mamy tutaj dostęp do zmiennej zmienna – elementy iterowalna_zmienna
}
Dict<string, int> imiona_lata;
wiek.add("Kasia", 22)
wiek.add(“Basia", 45);
for (Pair<string, int> para_im in imiona_lata) {
    print(“Imie: ” + para_im.first());
    print(“Wiek: ” + para_im.second());
} 
```
## Własne funkcje
Użytkownik może definiować własne funkcje, zawierające typ
1. Definiowanie własnej funkcji
```
function zwracany_typ nazwa_funkcji(lista_argumentów){
    #blok instrukcji
    return wartosc;
}
```
Możliwe jest także definiowanie funkcji, które nie zwracają żadnej
wartości- wtedy jako zwracany_typ używamy void.
Przykłady:
```
function int dodawanie(int a, int b) {
    int c = a + b;
    return c;
}
function void przywitanie(string imie) {
    print(“Witaj ” + name + “!”);
}
```
2. Przekazywanie argumentów do funkcji przez wartość
3. Język umożliwia rekursywne wywołania funkcji 
## Obsługa błędów:
### Wyjątki:

| Nazwa wyjątku                       | Opis                                                                                                       |
|-------------------------------------|------------------------------------------------------------------------------------------------------------|
| `WrongTypeError`                    | Występuje, gdy typ zmiennej nie jest zgodny z oczekiwanym typem.                                            |
| `DifferentTypesListError`           | Występuje, gdy lista zawiera elementy różnych typów.                                                        |
| `UndefinedVariableError`            | Występuje, gdy używana zmienna nie została zdefiniowana.                                                    |
| `WrongTypeReturnError`              | Występuje, gdy typ zwracany przez funkcję nie jest zgodny z oczekiwanym typem.                              |
| `FunctionAlreadyDefinedError`       | Występuje, gdy próbuje się zdefiniować funkcję, która już została zdefiniowana.                             |
| `FunctionNotDefinedError`           | Występuje, gdy wywołana funkcja nie została zdefiniowana.                                                   |
| `ZeroDivisionError`                 | Występuje, gdy następuje próba dzielenia przez zero.                                                        |
| `LexerException`                    | Ogólny wyjątek dla błędów leksykalnych zawierający informacje o linii i kolumnie błędu.                      |
| `CommentTooLongException`           | Występuje, gdy komentarz jest zbyt długi.                                                                   |
| `StringTooLongException`            | Występuje, gdy ciąg znaków jest zbyt długi.                                                                 |
| `IdentifierTooLongException`        | Występuje, gdy identyfikator jest zbyt długi.                                                               |
| `UnclosedStringException`           | Występuje, gdy ciąg znaków nie został zamknięty.                                                            |
| `NumberException`                   | Występuje, gdy liczba jest zbyt duża.                                                                       |
| `ParserException`                   | Ogólny wyjątek dla błędów parsowania zawierający informacje o linii i kolumnie błędu.                        |
| `SyntaxError`                       | Występuje, gdy składnia kodu jest niepoprawna.                                                              |
| `NoSemicolonError`                  | Występuje, gdy brakuje średnika w kodzie.                                                                   |
| `NoClosingCurlyBracketError`        | Występuje, gdy brakuje zamykającego nawiasu klamrowego w kodzie.                                            |
| `NoClosingBracketError`             | Występuje, gdy brakuje zamykającego nawiasu w kodzie.                                                       |
| `MaximumIterationsExceededError`| Błąd zgłaszany, gdy liczba iteracji przekracza maksymalną dopuszczalną wartość.                                      |
| `MaximumRecursionExceededError` | Błąd sygnalizujący, że maksymalna liczba rekursji została przekroczona.                                      |

### Wyjątki typów

- **`WrongTypeError`**
  - Tekst: "WrongTypeError: Expected type {expected}, but got {actual} at position {position}"

- **`DifferentTypesListError`**
  - Tekst: "DifferentTypesListError: Different types of elements at position {position}"

- **`UndefinedVariableError`**
  - Tekst: "UndefinedVariableError: Undefined variable {variable_name} at line: {position[0]} column: {position[1]}"

- **`WrongTypeReturnError`**
  - Tekst: "WrongTypeReturnError: Expected return type {expected}, but got {actual} at line: {position[0]} column: {position[1]}"

- **`FunctionAlreadyDefinedError`**
  - Tekst: "FunctionAlreadyDefinedError: Function {function_name} is already defined"

- **`FunctionNotDefinedError`**
  - Tekst: "FunctionNotDefinedError: Function {function_name} is not defined, line: {position[0]} at column: {position[1]}"

- **`ZeroDivisionError`**
  - Tekst: "ZeroDivisionError: Division by zero is not defined, line: {position[0]} at column: {position[1]}"

- **`MaximumIterationsExceededError`**
  - Tekst: "Błąd przekroczenia maksymalnej liczby iteracji: Przekroczono maksymalną liczbę iteracji, linia: {position[0]} kolumna: {position[1]}"

- **`MaximumRecursionExceededError`**
  - Tekst: "Błąd przekroczenia maksymalnej liczby rekursji: Przekroczono maksymalną liczbę rekursji, linia: {position[0]} kolumna: {position[1]}"
### Wyjątki leksykalne

- **`LexerException`**
  - Tekst: "LexerException: {message} in line:{line} column:{column}"

- **`CommentTooLongException`**
  - Tekst: "CommentTooLongException: {message} in line:{line} column:{column}"

- **`StringTooLongException`**
  - Tekst: "StringTooLongException: {message} in line:{line} column:{column}"

- **`IdentifierTooLongException`**
  - Tekst: "IdentifierTooLongException: {message} in line:{line} column:{column}"

- **`UnclosedStringException`**
  - Tekst: "UnclosedStringException: {message} in line:{line} column:{column}"

- **`NumberException`**
  - Tekst: "TooBigNumberException: {message} in line:{line} column:{column}"


### Wyjątki składniowe

- **`ParserException`**
  - Tekst: (brak specyficznego tekstu dla ogólnego wyjątku)

- **`SyntaxError`**
  - Tekst: "SyntaxError: Expected {message} in line:{line} column:{column}"

- **`NoSemicolonError`**
  - Tekst: "NoSemicolonError: Missing semicolon in line:{line} column:{column}"

- **`NoClosingCurlyBracketError`**
  - Tekst: "NoClosingCurlyBracketError: Missing closing curly bracket in line:{line} column:{column}"

- **`NoClosingBracketError`**
  - Tekst: "NoClosingBracketError: Missing closing bracket in line:{line} column:{column}"


## Testowanie:
Do testowania wykorzystam testy jednostkowe oraz integracyjne, napisane przy użyciu
frameworka pytest.
Test zostały zamieszczone w katalogu tests, podzielone dla testy dla danego modułu. 

17. Przykładowy kod

```
function int a(int b)
{
   if ( b + 2 > 7 ) { return b; }
   else { return 7; };
}

function List<string> linq_test(){
    Dict<int, string> ludzie = {19: "Kacper", 7: "Klara", 21: "Steve", 23: "Kamil"};
    List<string> adults = from Pair<int, string> para in ludzie where para.first() > 18 select para.second() orderby para.first();

    return adults;
}

function int print_hello(){
    int i = 10;
    while( i > 0 ) {
        print("Hello world!");
        i = i - 1;
    };
}

function int main(){
    # float a = 3.14;

    print([1, 2, 3]);
    List<int> lista = [1, 2, 3, 4];
    Pair<int, string> para = (1, "kacper");
    Dict<int, string> slownik = {1: "kacpi", 2: "tomek"};
    # slownik = slownik.add(3, "7");
    # print(slownik);
    # for (int a in lista) {
    #   print(a);
    # };

    return a(100);
}
```

## Typy tokenów
| Typ Tokena            | Opis                          |
|-----------------------|-------------------------------|
| `ID`                  | Identyfikator                 |
| `FUNCTION`            | Słowo kluczowe funkcji        |
| `INT_KEYWORD`         | Słowo kluczowe int            |
| `FLOAT_KEYWORD`       | Słowo kluczowe float          |
| `STRING_KEYWORD`      | Słowo kluczowe string         |
| `BOOL_KEYWORD`        | Słowo kluczowe bool           |
| `INT_VALUE`           | Wartość typu int              |
| `FLOAT_VALUE`         | Wartość typu float            |
| `STRING_VALUE`        | Wartość typu string           |
| `BOOL_VALUE`          | Wartość typu bool             |
| `PAIR`                | Słowo kluczowe pair           |
| `LIST`                | Słowo kluczowe list           |
| `DICT`                | Słowo kluczowe dict           |
| `LENGTH`              | Słowo kluczowe length         |
| `DELETE`              | Słowo kluczowe delete         |
| `GET`                 | Słowo kluczowe get            |
| `CONTAINS`            | Słowo kluczowe contains       |
| `TYPE`                | Słowo kluczowe type           |
| `AT`                  | Słowo kluczowe at             |
| `APPEND`              | Słowo kluczowe append         |
| `REMOVE`              | Słowo kluczowe remove         |
| `FIRST`               | Słowo kluczowe first          |
| `SECOND`              | Słowo kluczowe second         |
| `OR_SIGN`             | Znak or (`||`)                |
| `AND_SIGN`            | Znak and (`&&`)               |
| `LESS_SIGN`           | Znak mniejszości (`<`)        |
| `LESS_OR_EQUAL_SIGN`  | Znak mniejszy lub równy (`<=`)| 
| `GREATER_SIGN`        | Znak większości (`>`)         |
| `GREATER_OR_EQUAL_SIGN`| Znak większy lub równy (`>=`)|
| `EQUAL_SIGN`          | Znak równości (`==`)          |
| `NOT_EQUAL_SIGN`      | Znak nierówności (`!=`)       |
| `NEGATION_SIGN`       | Znak negacji (`!`)            |
| `ASSIGN`              | Znak przypisania (`=`)        |
| `LEFT_BRACKET`        | Lewy nawias okrągły (`(`)     |
| `RIGHT_BRACKET`       | Prawy nawias okrągły (`)`)    |
| `LEFT_CURLY_BRACKET`  | Lewy nawias klamrowy (`{`)    |
| `RIGHT_CURLY_BRACKET` | Prawy nawias klamrowy (`}`)   |
| `LEFT_SQUARE_BRACKET` | Lewy nawias kwadratowy (`[`)  |
| `RIGHT_SQUARE_BRACKET`| Prawy nawias kwadratowy (`]`) |
| `ADD_SIGN`            | Znak dodawania (`+`)          |
| `SUB_SIGN`            | Znak odejmowania (`-`)        |
| `MULTIPLY_SIGN`       | Znak mnożenia (`*`)           |
| `DIVIDE_SIGN`         | Znak dzielenia (`/`)          |
| `FOR`                 | Słowo kluczowe for            |
| `WHILE`               | Słowo kluczowe while          |
| `IF`                  | Słowo kluczowe if             |
| `ELSE`                | Słowo kluczowe else           |
| `RETURN`              | Słowo kluczowe return         |
| `KEY`                 | Słowo kluczowe key            |
| `FROM`                | Słowo kluczowe from           |
| `IN`                  | Słowo kluczowe in             |
| `WHERE`               | Słowo kluczowe where          |
| `SELECT`              | Słowo kluczowe select         |
| `ORDER_BY`            | Słowo kluczowe order by       |
| `TRUE_VALUE`          | Wartość true                  |
| `FALSE_VALUE`         | Wartość false                 |
| `SEMICOLON`           | Średnik (`;`)                 |
| `COLON`               | Dwukropek (`:`)               |
| `COMMA`               | Przecinek (`,`)               |
| `DOT`                 | Kropka (`.`)                  |
| `COMMENT`             | Komentarz                     |
| `EOF`                 | Koniec pliku                  |

## Węzły ast

| Typ węzła                 | Opis                                                                                           |
|---------------------------|------------------------------------------------------------------------------------------------|
| `Program`                 | Reprezentuje cały program, składający się z listy funkcji.                                      |
| `Variable`                | Reprezentuje zmienną z przypisaną nazwą.                                                        |
| `StatementBlock`          | Reprezentuje blok instrukcji.                                                                  |
| `SingleStatement`         | Reprezentuje pojedynczą instrukcję.                                                            |
| `BoolValue`               | Reprezentuje wartość logiczną (`True` lub `False`).                                            |
| `IntValue`                | Reprezentuje wartość całkowitą.                                                                |
| `FloatValue`              | Reprezentuje wartość zmiennoprzecinkową.                                                       |
| `StringValue`             | Reprezentuje wartość tekstową (ciąg znaków).                                                   |
| `Identifier`              | Reprezentuje identyfikator (nazwę zmiennej, funkcji, etc.).                                    |
| `Expression`              | Reprezentuje wyrażenie z lewym i prawym operatorem oraz operacją.                              |
| `FunctionBody`            | Reprezentuje ciało funkcji, składające się z treści oraz instrukcji `return`.                  |
| `FunctionCall`            | Reprezentuje wywołanie funkcji z listą argumentów.                                             |
| `MethodCall`              | Reprezentuje wywołanie metody z listą argumentów.                                              |
| `FunctionDefinition`      | Reprezentuje definicję funkcji, w tym jej typ zwracany, identyfikator, argumenty oraz ciało.   |
| `IfStatement`             | Reprezentuje instrukcję warunkową `if`, zawierającą warunek oraz bloki instrukcji dla prawdy i fałszu. |
| `Body`                    | Reprezentuje ogólny blok zawierający treść.                                                    |
| `ForStatement`            | Reprezentuje pętlę `for` z typem, identyfikatorem, kolekcją oraz ciałem pętli.                |
| `ForSortedStatement`      | Reprezentuje pętlę `for`, która iteruje po posortowanej kolekcji, z dodatkowym identyfikatorem klucza. |
| `WhileStatement`          | Reprezentuje pętlę `while` z warunkiem oraz ciałem pętli.                                      |
| `LINQ`                    | Reprezentuje zapytanie LINQ z instrukcjami `from`, `where`, `select` i `orderby`.              |
| `AndExpression`           | Reprezentuje wyrażenie logiczne AND.                                                           |
| `OrExpression`            | Reprezentuje wyrażenie logiczne OR.                                                            |
| `AddExpression`           | Reprezentuje wyrażenie dodawania.                                                              |
| `SubExpression`           | Reprezentuje wyrażenie odejmowania.                                                            |
| `MultiplyExpression`      | Reprezentuje wyrażenie mnożenia.                                                               |
| `DivisionExpression`      | Reprezentuje wyrażenie dzielenia.                                                              |
| `LessThanExpression`      | Reprezentuje wyrażenie mniejsze niż.                                                           |
| `LessThanOrEqualExpression` | Reprezentuje wyrażenie mniejsze lub równe.                                                 |
| `GreaterThanExpression`   | Reprezentuje wyrażenie większe niż.                                                            |
| `GreaterThanOrEqualExpression` | Reprezentuje wyrażenie większe lub równe.                                               |
| `EqualExpression`         | Reprezentuje wyrażenie równości.                                                              |
| `NotEqualExpression`      | Reprezentuje wyrażenie nierówności.                                                           |
| `Assignment`              | Reprezentuje przypisanie wartości do zmiennej.                                                |
| `Arguments`               | Reprezentuje listę argumentów przekazywanych do funkcji.                                       |
| `ReturnStatement`         | Reprezentuje instrukcję zwracania wartości z funkcji.                                          |
| `InitStatement`           | Reprezentuje inicjalizację zmiennej z przypisanym typem i wartością początkową.               |
| `Declaration`             | Reprezentuje deklarację zmiennej z przypisanym typem.                                         |
| `ListType`                | Reprezentuje typ listy z określonym typem elementów.                                           |
| `PairType`                | Reprezentuje typ pary z określonymi typami elementów.                                          |
| `DictType`                | Reprezentuje typ słownika z określonymi typami kluczy i wartości.                              |
| `IntType`                 | Reprezentuje typ całkowity.                                                                    |
| `StringType`              | Reprezentuje typ tekstowy.                                                                     |
| `FloatType`               | Reprezentuje typ zmiennoprzecinkowy.                                                           |
| `BoolType`                | Reprezentuje typ logiczny.                                                                     |
| `List`                    | Reprezentuje listę elementów.                                                                  |
| `Pair`                    | Reprezentuje parę elementów.                                                                   |


## Gramatyka
```
// część składniowa

program			= { function_declaration }
function_declaration	= "function", ( type_variable | "void" ) identifier function_params statement_block
function_params		= "(" [ type_variable identifier { "," type_variable identifier } ] ")"

statement_block		= "{" { statements } "}"
statements		= { single_statement semicolon_sign }

single_statement 	= for_loop 
			| if_statement
			| while_loop
			| return_statement
			| function_call
			| method_call
			| init_statement
			| init_container
			| assignment

function_call		= identifier arguments
method_call		= expression "." identifier "(" parameters ")"
if_statement		= "if" "(" expression ")" statement_block [ "else" statement_block ]
for_loop		= "for" "(" type_variable identifier "in" identifier ")" statement_block
for_loop_sorted		= "for" "(" type_variable identifier "in" identifier "," "key" "=" identifier ")" statement_block

parameters              = type_variable identifier {"," type_variable identifier} 

linq_query		= "from" type_variable identifier "in" identifier
			  "where" expression
			  "select" select_options
			  "orderby" expression

select_options		= identifier
			| function_call

return_statement	= "return" expression ";"
init_container		= type_container identifier ["=" "new" type_container "(" container_starter ")"]
init_statement		= type_basic identifier ["=" expression]
arguments		= "(" [ expression { "," expression } ] ")" semicolon_sign
assignable		= expression

assignment 		= (identifier, "=", expression)

container_starter	= "" 
			| container_inside
container_inside	= list_inside 
			| pair_inside
			| dict_inside
list_inside		= "[" text | number | container_inside {"," text | number | container_inside } "]"
pair_inside		= "[" text | number | container_inside "," text | number | container_inside  "]"
dict_inside		= "{" {  text | number | container_inside ":" text | number | container_inside  } "}"

expression 		= and_expression {or_sign expression}
and_expression 		= relation_expression {and_sign relation_expression}
relation_expression 	= sum_expression [relation_expression sum_expression]
sum_expression 		= multiply_expression {additive_sign multiplicative_expression}
multiply_expression 	= factor {multiplicative_sign factor}

factor 			= identifier 
			| function_call
			| method_call
			| constant 
constant 		= var_values
identifier		= letter { letter | digit }



// część leksykalna

type_variable		= type_basic
			| type_container

type_basic		= "int"
			| "float"
			| "string"
			| "bool"

type_container		= "List" "<" type_variable ">"
			| "Pair" "<" type_variable "," type_variable  ">"
			| "Dict""<" type_variable "," type_variable  ">"

or_sign			= "||"
and_sign		= "&&"
relation_sign		= "<" | "<=" | ">" | ">=" | "==" | "!="
additive_sign		= "+" | "-"
multiplicative_sign	= "*" | "/" | "%"
negation_sign		= "!"

var_values		= bool_value | decimal_value | string_value
bool_value		= true | false
decimal_value		= number
string_value		= text

true			= "true"
false			= "false"

text			= " { letter | number | white_space | nextline_sign | tab_sign } "
white_space		= " "
letter			= lowercase_letter | uppercase_letter
lowercase_letter	= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'
uppercase_letter	= 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'

nexline_sign		= backslash_sign "n"
tab_sign		= backslash_sign "t"

number			= '0' | ['-'] non_zero_digit { digit } ['.' digit { digit } ]
digit 			= '0' | non_zero_digit
non_zero_digit 		= '1' | '2' | '3' | '4' | '5' | '6'| '7' | '8' | '9'

semicolon_sign		= ";"
backslash_sign		= "/"
comment_start		= "#"
```

