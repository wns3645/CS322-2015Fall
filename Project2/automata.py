__author__ = 'JunHui'

"""
2015 Fall
Formal Languages and Automata

Project 2-1
20130273 JunHui Park
"""

## DFA(deterministic finite automaton)을 정의
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

    def rename(self):           ## DFA state의 이름을 보기 좋도록 바꿔준다(minimize하는 과정에서 이름이 복잡한 list로 구성되므로)
        n_state = []
        for i in self.state:
            n_state += [self.state.index(i)]

        n_trans = []
        for k in self.trans:
            n_trans += [[[self.state.index(k[0][0]), k[0][1]], self.state.index(k[1])]]

        n_initial = self.state.index(self.initial)

        n_final = []
        for t in self.final:
            n_final += [self.state.index(t)]

        n_final = list(set(n_final))

        self.state = n_state
        self.trans = n_trans
        self.initial = n_initial
        self. final = n_final

    def print_content(self, message):     ## DFA의 각 요소들을 format에 맞게 출력
        if message == 'dfa':
            print("#################DFA##################")
        elif message == 'mdfa':
            print("#################mDFA##################")
        print("State : ", end='')
        print(self.state)
        print("Vocabulary : ", end='')
        print(self.symbol)
        print("State Transition Functions : ")

        for i in self.trans:
            print(i[0], end='')
            print(" => ", end='')
            print(i[1])

        print("Initial State : ", end='')
        print(self.initial)
        print("Final State : ", end='')
        print(self.final)
        print()

    def minimize(self):

        m_state = []
        for i in self.state:
            m_state += [{i}]
        t_state = []

        m_symbol = self.symbol
        m_trans = []
        m_initial = self.initial
        m_final = []

        disting_set = []

        num_state = len(self.state)
        for i in range(0, num_state):
            for j in range(i+1, num_state):
                disting_set += [[{i, j}, 0]]

        ## final state를 포함하는 모든 원소를 distinguishable로 표시
        for k in self.final:
            for i in disting_set:
                if k in i[0]:
                    i[1] = 1
        ## final state끼리의 관계는 일단 not distinguishable로 표시
        for i in disting_set:
            if i[0] - set(self.final) == set():
                i[1] = 0

        ## distinguishable 한 state로 transition이 가능할 경우에도 distinguishable로 표시
        for k in range(0, len(disting_set)):
            for s in self.symbol:
                for i in range(0, len(disting_set)):
                    s_set = set()
                    count = 0
                    temp = disting_set[i][0]
                    temp = list(temp)
                    if disting_set[i][1] == 0:
                        for f in self.trans:
                            if f[0][0] == temp[0] and f[0][1] == s:
                                s_set.add(f[1])
                                count += 1
                            elif f[0][0] == temp[1] and f[0][1] == s:
                                s_set.add(f[1])
                                count += 1
                        if len(s_set) == 2:
                            for t in disting_set:
                                if s_set == t[0] and t[1] == 1:
                                    disting_set[i][1] = 1
                        elif count == 1:
                            disting_set[i][1] = 1

        t_flag = False

        ## equivalent한 state들을 하나의 state로 재정렬
        for i in disting_set:
            if i[1] == 0:
                t_state = []
                for k in m_state:
                    if (i[0] & k) != set():
                        if t_flag:
                            continue
                        else:
                            t_state += [(i[0] | k)]
                            t_flag = True
                    else:
                        t_state += [k]
                m_state = t_state
                t_flag = False

        for i in range(0, len(m_state)):
            m_state[i] = list(m_state[i])
            m_state[i].sort

        ## minimize된 state에 대해서 transition function도 재구성
        for i in m_state:
            for f in self.trans:
                if f[0][0] == i[0]:
                    for t in m_state:
                        try:
                            t.index(f[1])
                        except ValueError:
                            continue
                        else:
                            m_trans += [[[i, f[0][1]], t]]

        ## final state 재구성
        for i in m_state:
            for k in self.final:
                try:
                    i.index(k)
                except ValueError:
                    continue
                else:
                    m_final += [i]

        ## initial state 재구성
        for i in m_state:
            try:
                i.index(self.initial)
            except ValueError:
                continue
            else:
                m_initial = i

        self.state = m_state
        self.symbol = m_symbol
        self.trans = m_trans
        self.initial = m_initial
        self.final = m_final


## eNFA(epsilon nondeterministic finit automata)를 정의
## e-NFA는 nondeterministic(하나의 인풋 심볼로 여러개의 스테이트로 전이할 수 있음)하고 epsilon-transition(null string)을 허용한다
class eNFA:
    def __init__(self, state, symbol, trans, initial, final):
        self.state = state
        self.symbol = symbol
        self.trans = trans
        self.initial = initial
        self.final = final

    def print_content(self):     ## NFA의 각 요소들을 format에 맞게 출력
        print("#################eNFA##################")
        print("State : ", end='')
        print(self.state)
        print("Vocabulary : ", end='')
        print(self.symbol)
        print("State Transition Functions : ")

        for i in self.trans:
            print(i[0], end='')
            print(" => ", end='')
            print(i[1])

        print("Initial State : ", end='')
        print(self.initial)
        print("Final State : ", end='')
        print(self.final)
        print()

    def e_closure(self, state, trans):      ## epsilon-closure를 구한다

        result = [state]

        for i in trans:
            if i[0][0] == state and i[0][1] == 'eps':
                result += self.e_closure(i[1], trans)

        result = list(set(result))
        result.sort()

        return result

    def enfa_to_dfa(self):                  ## e-NFA를 DFA로 변환

        r_symbol = self.symbol
        r_trans = []
        r_final = []
        ## initial state 에 대한 epsilon closure를 구함
        r_initial = self.e_closure(self.initial, self.trans)
        ## epsilon clousre로 구한 initial state를 set of state에 넣는다
        r_state = [r_initial]

        new = True

        for i in r_state:
            for k in r_symbol:
                temp_closure = []
                new = True
                for t in i:
                    for j in self.trans:
                        if j[0][0] == t and j[0][1] == k:
                            temp_closure += self.e_closure(j[1], self.trans)
                if len(temp_closure) != 0:
                    temp_closure = list(set(temp_closure))
                    temp_closure.sort()
                    for c in r_state:
                        if c == temp_closure:
                            new = False
                            break
                    if new:
                        r_state += [temp_closure]
                        new = True
                    new = True
                    for f in r_trans:
                        if f == [[i, k], temp_closure]:
                            new = False
                            break
                    if new:
                        r_trans += [[[i, k], temp_closure]]
                        new = True
                else:
                    new = False

            for t in self.final:
                try:
                    i.index(t)
                except ValueError:
                    continue
                else:
                    r_final += [i]

        r_dfa = DFA(r_state, r_symbol, r_trans, r_initial, r_final)

        return r_dfa



## input을 받아서 e-NFA 작성

if __name__ == "__main__":
    state = input()
    state = state.split()

    symbol = input()
    symbol = symbol.split()

    trans_en = []
    while True:
        trans = input()
        if trans == 'end':
            break
        else:
            trans = trans.split()
            pop = trans.pop()
            trans = [trans, pop]
            trans_en.append(trans)

    initial = input()
    final = input()
    final = final.split()

    in_enfa = eNFA(state, symbol, trans_en, initial, final)

    ## e_NFA를 dfa로 변환하여 새로운 DFA작성
    out_dfa = in_enfa.enfa_to_dfa()

    out_dfa.rename()
    out_dfa.print_content('dfa')

    ## dfa 를 minimize
    out_dfa.minimize()
    out_dfa.rename()
    out_dfa.print_content('mdfa')

    a = input("check accepting : ")
    out_dfa.accept(a)






