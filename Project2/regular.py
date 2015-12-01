__author__ = "Junhui"

"""
2015 Fall, KAIST
CS322, Formal Language and Automata Therory


Project 2

20130273 Junhui Park
"""


tokens = ('SIM', 'LPAREN', 'RPAREN', 'UNION', 'CONCATE', 'CLOSURE', 'EPSILON')

## Tokens

t_UNION = r'\+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_CLOSURE = r'\*'
t_CONCATE = r'.'

reserved = {
		'eps' : 'EPSILON'
		}

def t_SIM(t):
	r'[a-zA-z_][a-zA-Z0-9]*'
	t.type = reserved.get(t.value, 'SIM')
	return t

t_ignore = " \t"

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


## Build a lexer

## import 예비프로젝트 2-1
import automata as fa

state = list()
symbol = list()
trans = list()
initial = 's'
final = list()


import ply.lex as lex
lexer = lex.lex()

## Parsing rules

precedence = (	
		('left', 'UNION'),
		('left', 'CONCATE'),
		('left', 'CLOSURE'),
		('nonassoc', 'SIM', 'EPSILON'),
		)

def p_expr_group(t):
	'expr : LPAREN expr RPAREN'
	t[0] = t[2]

def p_expr_union(t):
	'expr : expr UNION expr'
	state = t[1].state
	symbol = t[1].symbol
	trans = t[1].trans 
	
	for i in range(0, len(t[3].state)):
		state.append(t[3].state[i] + t[1].final[0])
	
	state += [t[3].final[0] + t[1].final[0] + 1, t[3].final[0] + t[1].final[0] + 2]
	state.sort()
	
	initial = t[3].final[0] + t[1].final[0] + 1
	final = [t[3].final[0] + t[1].final[0] + 2]

	symbol += t[3].symbol
	symbol = list(set(symbol))
	symbol.sort()

	for i in range(0, len(t[3].trans)):
		trans.append([[t[3].trans[i][0][0] + t[1].final[0], t[3].trans[i][0][1]], t[3].trans[i][1] + t[1].final[0]])
	trans.append([[initial, 'eps'], t[1].initial])
	trans.append([[initial, 'eps'], t[3].initial + t[1].final[0]])
	trans.append([[t[1].final[0], 'eps'], final[0]])
	trans.append([[t[3].final[0] + t[1].final[0], 'eps'], final[0]])

	t[0] = fa.eNFA(state, symbol, trans, initial, final)	

def p_expr_concate(t):
	'expr : expr CONCATE expr'
	initial = t[1].initial
	state = t[1].state
	symbol = t[1].symbol
	trans = t[1].trans 
	
	for i in range(0, len(t[3].state)):
		state.append(t[3].state[i] + t[1].final[0])
	state.sort()

	symbol += t[3].symbol
	symbol = list(set(symbol))
	symbol.sort()

	for i in range(0, len(t[3].trans)):
		trans.append([[t[3].trans[i][0][0] + t[1].final[0], t[3].trans[i][0][1]], t[3].trans[i][1] + t[1].final[0]])
	trans.append([[t[1].final[0], 'eps'], t[3].initial + t[1].final[0]])
	
	final = [t[3].final[0] + t[1].final[0]]

	t[0] = fa.eNFA(state, symbol, trans, initial, final)

def p_expr_closure(t):
	'expr : expr CLOSURE'
	initial = t[1].initial
	state = t[1].state
	symbol = t[1].symbol
	trans = t[1].trans
	final = t[1].final
	
	state += [final[0]+ 1, final[0]+2]
	state.sort()
	
	initial = final[0]+ 1
	final = [final[0] + 2]

	trans += [[[initial, 'eps'], t[1].initial], [[initial, 'eps'], final[0]], [[t[1].final[0], 'eps'], t[1].initial], [[t[1].final[0], 'eps'], final[0]]]

	t[0] = fa.eNFA(state, symbol, trans, initial, final)

def p_expr_eps(t):
	'expr : EPSILON'
	t[0] = fa.eNFA([1, 2], [], [[[1, 'eps'], 2]], 1, [2])

def p_expr_sym(t):
	'expr : SIM'
	t[0] = fa.eNFA([1, 2], [t[1]], [[[1, t[1]], 2]], 1, [2])

def p_error(t):
	print("Syntax not correct '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()


while True:
	try:
		s = input("input : ")
	except EOFError:
		break
	##### class를 상속시켜서 여기에 e-NFA를 선언하고, 각 함수의 호출 때마다 e-NFA를 수정할 수 있도록 한다.(state, symbol, transition functions등등...) 이렇게 결과적으로 만들어진  e-NFA를 다시 minimize하면 끝!!! --->> 클래스 상속에 대해서 공부해보고, e-NFA의 내용을 계속해서 변경할 수 있는지 확인, 변경할 수 없다면 변경할 수 있도록 클래스의 함수를 생성하거나 변수를 static하게 선언하여 바꿔버리자!! 내일한다! 
	t = parser.parse(s)
	t.print_content()

	dfa_t = t.enfa_to_dfa()
	dfa_t.rename()
	dfa_t.print_content('dfa')

	dfa_t.minimize()
	dfa_t.rename()
	dfa_t.print_content('mdfa')

