__author__ = 'JunHui'

"""
2015 Fall
Formal Languages and Automata

Project 1-1
20130273 JunHui Park
"""


# DFA(deterministic finite automaton)을 정의
class DFA:

    def __init__(self, state, symbol, trans, initial, final):
        self.state = state
        self.symbol = symbol
        self.trans = trans
        self.initial = initial
        self.final = final


    def accept(self, a):
        current = self.initial
        accept = False
        dead = True


        for i in a:
            try:
                self.symbol.index(i)
            except ValueError as e:
                print(e)
                return

            for f in self.trans:
                if f[0][0] == current and f[0][1] == i:
                    current = f[1]
                    dead = False
                    break

            if dead == True:
                print("아니오")
                return

        for k in self.final:
            if current == k:
                accept = True
                break

        if accept:
            print("네")
        else:
            print("아니오")

