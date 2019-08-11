HTML_HEAD = '''
<!DOCTYPE html>
<html lang="en">
<html>
<head>
<title>IPUZ Viewer</title>
<style>
.box {
  float: left;
  padding: 10px;
}
.clearfix::after {
  content: "";
  clear: both;
  display: table;
}
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

HTML_HEADING = '<h{hd}>{0}</h{hd}>'

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
    
    def finalize(self):
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

    def container_begin(self):
        print('<div class="clearfix">', file=self.html_file)

    def container_end(self):
        print('</div>', file=self.html_file)

    def box_begin(self):
        print('<div class="box">', file=self.html_file)

    def box_end(self):
        print('</div>', file=self.html_file)
        
    def heading(self, level, text):
        '''Draw heading'''
        print(HTML_HEADING.format(text, hd=level), file=self.html_file)

    def line(self, text):
        '''Draw a single line with terminator'''
        print(text+'<br>', file=self.html_file)
    
    def rights(self, text):
        '''Draw acknowledgements'''
        print('<p>&copy; Copyright {}</p>'.format(text), file=self.html_file)
    