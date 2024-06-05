function int a(int b)
{
   if ( b + 2 > 7 ) { return 10; }
   else { return 7; };
}

function List<string> linq_test(){
    Dict<int, string> ludzie = {19: "Kacper", 7: "Klara", 21: "Steve", 23: "Kamil"};
    List<string> adults = from Pair<int, string> para in ludzie where para.first() > 18 select para.second() orderby para.first();

    return adults;
}

function int print_hello(){
    int i = 10;
    while( 10 > 0 ) {
        print("Hello world!");
    };
}

function int main(){
    # float a = 3.14;

    # print([1, 2, 3]);
    List<int> lista = [1, 2, 3, 4];
    Pair<int, string> para = (1, "kacper");
    Dict<int, string> slownik = {1: "kacpi", 2: "tomek"};
    # slownik = slownik.add(3, "7");
    # print(slownik);
    for (int a in lista) {
       print(a + 1);
    };
    # print(linq_test());
    # print(lista);
    #print(para.second());
    # print(slownik);
    print_hello();
    print(linq_test());
    #int b = 3;
    #print(10);
    return a(1);
}


function int main_1(){
    int a = 10;
    return a;
}