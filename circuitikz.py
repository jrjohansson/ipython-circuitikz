"""
An IPython extension for generating circuit diagrams using LaTeX/Circuitikz
from within ipython notebook.
"""
import os
from IPython.core.magic import magics_class, cell_magic, Magics
from IPython.display import Image, SVG

latex_template = r"""
\documentclass{minimal}
\usepackage[paperwidth=%s,paperheight=%s,margin=0in]{geometry}
\usepackage{tikz}
\usepackage[%s]{circuitikz}
\begin{document}
\begin{center}
%s
\end{center}
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
                paperwidth = 8in
                paperheight = 6in
                dpi = 100
                options = europeanresistors,americaninductors

        """
        options = {'filename': 'ipynb-circuitikz-output',
                   'paperwidth': '8in',
                   'paperheight': '6in',
                   'dpi': '100',
                   'options': 'europeanresistors,americaninductors'}


        for option in line.split(" "):
            key, value = option.split("=")
            if key in options:
                options[key] = value
            else:
                print("Unrecongized option %s" % key)

        filename = options['filename']
        code = cell

        os.system("rm -f %s.tex %s.pdf %s.png" % (filename, filename, filename))        

        with open(filename + ".tex", "w") as file:
            file.write(latex_template % (options['paperwidth'],
                                         options['paperheight'], 
                                         options['options'], 
                                         cell))
    
        os.system("pdflatex %s.tex" % filename)
        os.system("rm -f %s.aux %s.log" % (filename, filename))        
        os.system("convert -density %s %s.pdf %s.png" % (options['dpi'], filename, filename))
        img = Image(filename + ".png")
        return img


def load_ipython_extension(ipython):
    ipython.register_magics(Circuitikz)
