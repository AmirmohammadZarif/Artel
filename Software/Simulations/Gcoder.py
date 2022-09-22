from pygcode import Line
from pygcode import Machine, GCodeRapidMove
with open('test.gcode', 'r') as fh:
    for line_text in fh.readlines():
        line = Line(line_text)
        code = "X100 Y20 Z120 \n X102 Y230 Z120"
        print(line) 
        # line.block.gcodes 
        print(code.split(' '))
        print(code.split('\n'))
        # print(line.block.modal_params)
        # if line.comment:
            # print(line.comment.text)