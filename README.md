# KacperScript - projekt tkom
## Dokumentacja końcowa

Celem projektu było stworzenie języka, oferującego podstawowe własności
języków programowania wraz z wbudowanym typem słownika.
Dostępne operacje na słowniku:
- dodawanie elementów
- usuwanie elementów
- wyszukiwanie elementów według klucza
- iterowanie po elementach zgodnie z zadaną kolejnością
- wykonanie na słowniku zapytań w stylu LINQ

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
- z int na float
- z float na int.
Pierwszy przypadek jest prostszy, do liczby całkowitej zostaje dodana
część ułamkowa równa 0. W drugim przypadku zaś, część ułamkowa
zostaje wycięta, pozostaje jedynie część całkowita.
```
int x = 10;
float y = float(x); # y = 10.0
float a = 5.9;
int b = int(a); # b = 5
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
1) Błąd składniowy
Przykład:
int a = 10;
if (a == 10) { print(“10”);
[ERROR] Syntax error: missing “}” at line 23
int przywitanie() {
print(“Hello world!”)
}
[ERROR] Syntax error: missing “;” at line 42
b) Błąd dzielenia przez 0
Przykład:
print(10 / 0);
[ERROR] Dividing by zero: 10/0 at line 32
c) Błąd w indeksowaniu
list[int] = new list([1,2,3])
print(list.at(4))
[ERROR] Index error: list index out of range at line 87
d) Błąd w konwersji typów
string imie = “Kacper”;
int imie_int = int(imie);
[ERROR] Value error: invalid literal for int(): “kacper”
e) Zła ilość argumentów przekazanych do funkcji:
function void przywitanie(string imie) {
print(“Witaj” + imie + “!”);
}
przywitanie(“Kacper”, “Murygin”)
[ERROR] Function error: Wrong number of arguments- 2 instead of 1:
line 5 
## Testowanie:
Do testowania wykorzystam testy jednostkowe oraz integracyjne, napisane przy użyciu
frameworka pytest.
Test zostały zamieszczone w katalogu tests, podzielone dla testy dla danego modułu. 
## Sposób uruchomienia interpreter:
Uruchamiamy poprzez komendę:
./main.py <sciezka do pliku>
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
comment_start		= "//"
```

