HTML_HEAD = '''
<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
  border: 1px solid black;
}
th, td {
  padding: 5px;
}
#blockcell {
  background-color: black;
}
</style>
</head>
<body>
'''

HTML_TAIL = '''
</body>
</html>
'''

HTML_TABLE_OPEN  = '<table>'
HTML_TABLE_CLOSE = '</table>'

HTML_TABLE_ROW_OPEN  = '<tr">'
HTML_TABLE_ROW_CLOSE = '</tr>'

HTML_TABLE_CELL = '<td{bg}><small><sup>{0}</sup></small>{1}</td>'

BLOCKCELL_DEFAULT_ID = '#'


class Render:
    def __init__(self, html_file_name, blockcell_id=None):
        if blockcell_id is None:
            self.blockcell_id = BLOCKCELL_DEFAULT_ID
        else:
            self.blockcell_id = blockcell_id
        self.html_file_name = html_file_name
        self.html_file = open(html_file_name, 'w')
        self.html_file.write(HTML_HEAD)
    
    def close(self):
        self.html_file.write(HTML_TAIL)
        self.html_file.close()

    def grid_begin(self):
        print(HTML_TABLE_OPEN, file=self.html_file)

    def grid_end(self):
        print(HTML_TABLE_CLOSE, file=self.html_file)

    def grid_append(self, row):
        '''row is a list of tuple (apex, solution)'''
        print(HTML_TABLE_ROW_OPEN, file=self.html_file)
        for cell in row:
            color = ''  # default
            apex = cell[0]
            solution = cell[1]
            if apex == self.blockcell_id:
                color = ' id="blockcell"'
            elif apex == 0:
                apex = '&nbsp;&nbsp;'
            else:
                apex = '{}'.format(apex)
                if len(apex) < 2:
                    apex = '&nbsp;' + apex
            if solution == ' ':
                solution = '&nbsp;'
            print(HTML_TABLE_CELL.format(apex, solution, bg=color), file=self.html_file)
        print(HTML_TABLE_ROW_CLOSE, file=self.html_file)
    