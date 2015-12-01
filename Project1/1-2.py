__author__ = 'JunHui'


"""
20 15 Fall
Formal Languages and Automata

Project 1-2
10.01.2015
20130273 JunHui Park
"""

class Mealy:

    def __init__(self, state, symbol, out_symbol, trans, out_function, initial):
        self.state = state
        self.symbol = symbol
        self.out_symbol = out_symbol
        self.trans = trans
        self.out_function = out_function
        self.initial = initial


    def result(self, a):
        current = self.initial     #current state
        next = self.initial        #next state
        dead = True                #dead state


        for i in a:
            try:
                self.symbol.index(i)
            except ValueError as e:
                print(e)
                return

            for f in self.trans:
                if f[0][0] == current and f[0][1] == i:
                    next = f[1]
                    dead = False
                    break

            for o in self.out_function:
                if o[0][0] == current and o[0][1] == i:
                    print(o[1], end = '')
                    break

            current = next

            if dead == True:
                print("not proper input")
                return

        print('')








