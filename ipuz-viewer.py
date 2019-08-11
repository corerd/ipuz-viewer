import crossword
import ipuz

from render import Render

# Paths relative to VsCode workspace folder
PUZZLE_FILE = 'ipuz-viewer/fixtures/ipuz/example.ipuz'
HTML_FILE = 'crossword.html'


def get_literal(cell_value):
    '''Return the cell literal value

    An IPUZ formatted cell may contain
        - literals, that is numbers or strings rapresenting numbers
          (e.g., both 1 and "1" are the same);
        - a JSON dictionary, where the value key is 'cell'.
    See: http://www.ipuz.org/
    '''
    try:
        cell_value = cell_value['cell']
    except TypeError:
        # value is already a literal
        pass
    return cell_value


def viewer():
    with open(PUZZLE_FILE) as puzzle_file:
        ipuz_dict = ipuz.read(puzzle_file.read())  # may raise ipuz.IPUZException    
    puzzle = crossword.from_ipuz(ipuz_dict)

    html = Render(HTML_FILE, puzzle.block)

    # draw crossword board
    html.grid_begin()
    for row in puzzle:
        html.grid_append([(get_literal(cell.puzzle), ' ') for cell in row])
    html.grid_end()

    # draw solution
    html.grid_begin()
    for row in puzzle:
        html.grid_append([(get_literal(cell.puzzle), cell.solution) for cell in row])
    html.grid_end()

    html.close()
    print('Generate:', PUZZLE_FILE)

    return 0


if __name__ == "__main__":
    exit(viewer())