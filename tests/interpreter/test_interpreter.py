import io

from src.interpreter.interpreter import Interpreter
from src.parser.parser import Parser
from src.reader import Reader
from src.lexer.lexer import Lexer, get_tokens


def create_parser(string):
    reader = Reader(io.StringIO(string))
    lexer = Lexer(reader)
    return Parser(reader, lexer)


def get_return_value_from_main(string):
    parser = create_parser(string)
    program = parser.parse()
    interpreter = Interpreter(program)
    return interpreter.visit_program()


def test_simple_main():
    string = 'function int main(){return 3+1;}'
    result = get_return_value_from_main(string)
    assert result == 4


def test_function_call_1():
    string = """
    function int a(int b){return b + 4 * 5;}
    function int main(){return a(2) + 10;}
    """
    result = get_return_value_from_main(string)
    assert result == 32


def test_init_statement():
    string = """
    function int main(){int a = 10; return a;}
    """
    result = get_return_value_from_main(string)
    assert result == 10


def test_list():
    string = """
    function List<int> main(){return [1, 2, 3];}
    """
    result = get_return_value_from_main(string)
    assert result == [1, 2, 3]


def test_pair():
    string = """
    function int main(){return (1, 3);}
    """
    result = get_return_value_from_main(string)
    assert result == (1, 3)


def test_dict():
    string = """
    function int main(){return {1: 39, 2: 45};}
    """
    result = get_return_value_from_main(string)
    assert result == {1: 39, 2: 45}


def test_if_true():
    string = """
    function int main(){ if(true) { return 10; } else { return 7; };}
    """
    result = get_return_value_from_main(string)
    assert result == 10


def test_if_falss():
    string = """
    function int main(){ if(false) { return 10; } else { return 7; };}
    """
    result = get_return_value_from_main(string)
    assert result == 7


def test_if_condition():
    string = """
    function int main(){ if( 10 < 20) { return "C++"; } else { return "Python"; };}
    """
    result = get_return_value_from_main(string)
    assert result == "C++"


def test_while():
    string = """
    function int main(){ while(17 > 10) { return 10; };}
    """
    result = get_return_value_from_main(string)
    assert result == 10


def test_dictionary_length():
    string = """
    function int main(){ return {1: 2, 2: 3}.length(); }
    """
    result = get_return_value_from_main(string)
    assert result == 2


def test_dictionary_add():
    string = """
    function int main(){ return {1: 2, 2: 3}.add(3, 4); }
    """
    result = get_return_value_from_main(string)
    assert result == {1: 2, 2: 3, 3: 4}


def test_dictionary_delete():
    string = """
    function int main(){ return {1: 2, 2: 3}.delete(2); }
    """
    result = get_return_value_from_main(string)
    assert result == {1: 2}


def test_dictionary_get():
    string = """
    function int main(){ return {1: 2, 2: 3}.get(2); }
    """
    result = get_return_value_from_main(string)
    assert result == 3


def test_dictionary_contains():
    string = """
    function int main(){ return {1: 2, 2: 3}.contains(2024); }
    """
    result = get_return_value_from_main(string)
    assert result is False


def test_pair_first():
    string = """
    function int main(){ return ("Warszawa", "Łódź").first(); }
    """
    result = get_return_value_from_main(string)
    assert result == "Warszawa"


def test_pair_second():
    string = """
    function int main(){ return ("Warszawa", "Łódź").second(); }
    """
    result = get_return_value_from_main(string)
    assert result == "Łódź"


def test_list_length():
    string = """
    function int main(){ return ["Warszawa", "Łódź", "Gdańsk"].length(); }
    """
    result = get_return_value_from_main(string)
    assert result == 3


def test_list_type():
    string = """
    function int main(){ return ["Warszawa", "Łódź", "Gdańsk"].type(); }
    """
    result = get_return_value_from_main(string)
    assert result == str


def test_list_at():
    string = """
    function int main(){ return ["Warszawa", "Łódź", "Gdańsk"].at(2); }
    """
    result = get_return_value_from_main(string)
    assert result == "Gdańsk"


def test_list_append():
    string = """
    function int main(){ return ["Warszawa", "Łódź", "Gdańsk"].append("Kraków"); }
    """
    result = get_return_value_from_main(string)
    assert result == ["Warszawa", "Łódź", "Gdańsk", "Kraków"]


def test_list_remove():
    string = """
    function List<string> main(){ List<string> lista = ["Warszawa", "Łódź", "Gdańsk"]; return lista.remove("Warszawa"); }
    """
    result = get_return_value_from_main(string)
    assert result == ["Łódź", "Gdańsk"]


def test_linq_query():
    string = """
    function int main(){ Dict<int, string> ludzie = {19: "Kacper"}; List<string> adults = from Pair<int, string> para in ludzie where para.first() > 18 select para.second() orderby para.first(); return adults;}
    """
    result = get_return_value_from_main(string)
    assert result == ""
