"""
An IPython extension for generating circuit diagrams using LaTeX/Circuitikz
from within ipython notebook.
"""
import os
from IPython.core.magic import magics_class, cell_magic, Magics
from IPython.display import Image, SVG

#%\usepackage[paperwidth=%s,paperheight=%s,margin=0in]{geometry}
latex_template = r"""\documentclass{standalone}
\usepackage{tikz}
\usepackage[%s]{circuitikz}
\begin{document}
%s
\end{document}
"""

@magics_class
class Circuitikz(Magics):

    @cell_magic
    def circuitikz(self, line, cell):
        """Generate and display a circuit diagram using LaTeX/Circuitikz.
        
        Usage:
        
            %circuitikz [key1=value1] [key2=value2] ...

            Possible keys and default values are

                filename = ipynb-circuitikz-output
                dpi = 100 (for use with format = png)
                options = europeanresistors,americaninductors
                format = svg (svg or png)

        """
        options = {'filename': 'ipynb-circuitikz-output',
                   'dpi': '100',
                   'format': 'png',
                   'options': 'europeanresistors,americaninductors'}


        for option in line.split(" "):
            try:
                key, value = option.split("=")
                if key in options:
                    options[key] = value
                else:
                    print("Unrecongized option %s" % key)
            except:
                pass

        filename = options['filename']
        code = cell

        os.system("rm -f %s.tex %s.pdf %s.png" % (filename, filename, filename))        

        with open(filename + ".tex", "w") as file:
            file.write(latex_template % (options['options'], cell))
    
        os.system("pdflatex -interaction batchmode %s.tex" % filename)
        os.system("rm -f %s.aux %s.log" % (filename, filename))        
        os.system("pdfcrop %s.pdf %s-tmp.pdf" % (filename, filename))
        os.system("mv %s-tmp.pdf %s.pdf" % (filename, filename))        

        if options['format'] == 'png':
            os.system("convert -density %s %s.pdf %s.png" % (options['dpi'], filename, filename))
            result = Image(filename=filename + ".png")
        else:
            os.system("pdf2svg %s.pdf %s.svg" % (filename, filename))
            result = SVG(filename + ".svg")

        return result


def load_ipython_extension(ipython):
    ipython.register_magics(Circuitikz)
