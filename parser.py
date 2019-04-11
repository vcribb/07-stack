from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:

         push: push a copy of the current top of the coordinate system stack to the stack

         pop: pop off the current top of the coordinate system stack
"""
ARG_COMMANDS = [ 'box', 'sphere', 'torus', 'circle', 'bezier', 'hermite', 'line', 'scale', 'move', 'rotate', 'save' ]

def parse_file(fname, edges, polygons, csystems, screen, color):
    #print(len(csystems))
    #print(csystems)

    f = open(fname)
    lines = f.readlines()

    step = 100
    step_3d = 20

    c = 0
    while c < len(lines):
        line = lines[c].strip()

        if line in ARG_COMMANDS:
            c+= 1
            args = lines[c].strip().split(' ')

        if line == 'push':
            temp = [item for item in csystems[-1]]
            csystems.append(temp)

        elif line == 'pop':
            csystems.pop()

        elif line == 'sphere':
            add_sphere(polygons,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult(csystems[-1], polygons)
            draw_polygons(polygons, screen, color)
            polygons = []

        elif line == 'torus':
            add_torus(polygons,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult(csystems[-1], polygons)
            draw_polygons(polygons, screen, color)
            polygons = []

        elif line == 'box':
            add_box(polygons,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(csystems[-1], polygons)
            draw_polygons(polygons, screen, color)
            polygons = []

        elif line == 'circle':
            add_circle(edges,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult(csystems[-1], edges)
            draw_lines(edges, screen, color)
            edges = []

        elif line == 'hermite' or line == 'bezier':
            add_curve(edges,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      step, line)
            matrix_mult(csystems[-1], edges)
            draw_lines(edges, screen, color)
            edges = []

        elif line == 'line':
            add_edge(edges,
                     float(args[0]), float(args[1]), float(args[2]),
                     float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(csystems[-1], edges)
            draw_lines(edges, screen, color)
            edges = []

        elif line == 'scale':
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(csystems[-1], edges)
            csystems[-1] = t

        elif line == 'move':
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(csystems[-1], t)
            csystems[-1] = t

        elif line == 'rotate':
            theta = float(args[1]) * (math.pi / 180)

            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(csystems[-1], t)
            csystems[-1] = t

        elif line == 'ident':
            ident(transform)

        elif line == 'apply':
            matrix_mult( transform, edges )
            matrix_mult( transform, polygons )

        elif line == 'clear':
            edges = []
            polygons = []

        elif line == 'display' or line == 'save':
            #clear_screen(screen)
            #draw_lines(edges, screen, color)
            #draw_polygons(polygons, screen, color)

            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
        c+= 1
