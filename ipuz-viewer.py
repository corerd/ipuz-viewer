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

    draw = Render(HTML_FILE, puzzle.block)
    draw.heading(1, 'Crossword example')
    draw.heading(2, '{} by {}'.format(puzzle.meta['title'], puzzle.meta['publisher']))

    # draw crossword board
    draw.grid_begin()
    for row in puzzle:
        draw.grid_append([(get_literal(cell.puzzle), ' ') for cell in row])
    draw.grid_end()

    # container to hold clues
    draw.container_begin()

    # disply ACROSS clues
    draw.box_begin()
    draw.heading(3, 'ACROSS')
    for number, clue in puzzle.clues.across():
        draw.line('{} {}'.format(number, clue))
    draw.box_end()
    
    # disply DOWN clues
    draw.box_begin()
    draw.heading(3, 'DOWN')
    for number, clue in puzzle.clues.down():
        draw.line('{} {}'.format(number, clue))
    draw.box_end()

    draw.container_end()

    # draw solution
    draw.heading(2, 'Solution')
    draw.grid_begin()
    for row in puzzle:
        draw.grid_append([(get_literal(cell.puzzle), cell.solution) for cell in row])
    draw.grid_end()

    draw.rights(puzzle.meta['rights'])

    draw.finalize()
    print('Generate:', PUZZLE_FILE)

    return 0


if __name__ == "__main__":
    exit(viewer())