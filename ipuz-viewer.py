import crossword
import ipuz

from htmlpage import HtmlPage


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


def viewer(ipuz_file_name, rendered_file_name):
    with open(ipuz_file_name) as puzzle_file:
        ipuz_dict = ipuz.read(puzzle_file.read())  # may raise ipuz.IPUZException    
    puzzle = crossword.from_ipuz(ipuz_dict)

    with HtmlPage(rendered_file_name) as draw:
        draw.heading(1, 'Crossword example')
        draw.heading(2, '{} by {}'.format(puzzle.meta['title'], puzzle.meta['publisher']))

        # draw the empty crossword board
        with draw.crossword(puzzle.block) as grid:
            for row in puzzle:
                grid.add_row([(get_literal(cell.puzzle), ' ') for cell in row])

        # container to hold clues
        with draw.column_container() as _:
            # disply ACROSS clues
            with draw.column() as _:
                draw.heading(3, 'ACROSS')
                for number, clue in puzzle.clues.across():
                    draw.line('{} {}'.format(number, clue))
            
            # disply DOWN clues
            with draw.column() as _:
                draw.heading(3, 'DOWN')
                for number, clue in puzzle.clues.down():
                    draw.line('{} {}'.format(number, clue))

        # draw solution
        draw.heading(2, 'Solution')
        with draw.crossword(puzzle.block) as grid:
            for row in puzzle:
                grid.add_row([(get_literal(cell.puzzle), cell.solution) for cell in row])

        draw.rights(puzzle.meta['rights'])


if __name__ == "__main__":
    print('Converting IPUZ to HTML...')

    # Paths relative to VsCode workspace folder
    viewer( 'ipuz-viewer/fixtures/ipuz/example.ipuz',
            'crossword.html' )
    print('Done!')
