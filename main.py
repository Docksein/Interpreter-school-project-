from InputStream import InputStream
from LexicalAnalysis import Tokenizer
from SyntacticAnalysis import Parser

# Incializujeme tokenizer s naším zdrojovým kódem.
tokenizer = Tokenizer(InputStream.from_file("source.gjk"))

# Incializujeme parser.
parser = Parser(tokenizer)

# Provedeme parsing (syntaktickou a sémantickou analýzu) a
# vytvoříme abstraktní syntaktický strom.
ast = parser.parse()

print(ast)

# Vytvoříme si tabulku symbolů, která udržuje informace
# o názvech a hodnotách všech proměnných a funkcí.
symbol_table = dict()

# Interpretujeme vrácený syntaktický strom.
ast.evaluate(symbol_table)
   