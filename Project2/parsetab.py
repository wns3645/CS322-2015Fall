
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '2F32B8413F5F9B727789AC714F752AEF'
    
_lr_action_items = {'LPAREN':([0,1,7,8,],[1,1,1,1,]),'EPSILON':([0,1,7,8,],[2,2,2,2,]),'UNION':([2,3,4,5,6,9,10,11,],[-5,8,-6,8,-4,-1,-3,-2,]),'CLOSURE':([2,3,4,5,6,9,10,11,],[-5,6,-6,6,-4,-1,6,6,]),'CONCATE':([2,3,4,5,6,9,10,11,],[-5,7,-6,7,-4,-1,-3,7,]),'SIM':([0,1,7,8,],[4,4,4,4,]),'$end':([2,3,4,6,9,10,11,],[-5,0,-6,-4,-1,-3,-2,]),'RPAREN':([2,4,5,6,9,10,11,],[-5,-6,9,-4,-1,-3,-2,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expr':([0,1,7,8,],[3,5,10,11,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expr","S'",1,None,None,None),
  ('expr -> LPAREN expr RPAREN','expr',3,'p_expr_group','regular.py',65),
  ('expr -> expr UNION expr','expr',3,'p_expr_union','regular.py',69),
  ('expr -> expr CONCATE expr','expr',3,'p_expr_concate','regular.py',97),
  ('expr -> expr CLOSURE','expr',2,'p_expr_closure','regular.py',120),
  ('expr -> EPSILON','expr',1,'p_expr_eps','regular.py',138),
  ('expr -> SIM','expr',1,'p_expr_sym','regular.py',142),
]
