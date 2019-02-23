
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "left+>NAME NUMBERstatement : expressionexpression : expression '+' expression\n                  | expression '>' expressionexpression : '(' expression ')'expression : NAME"
    
_lr_action_items = {'NAME':([0,2,6,7,],[1,1,1,1,]),')':([1,5,8,9,10,],[-5,8,-4,-2,-3,]),'(':([0,2,6,7,],[2,2,2,2,]),'+':([1,4,5,8,9,10,],[-5,6,6,-4,-2,-3,]),'$end':([1,3,4,8,9,10,],[-5,0,-1,-4,-2,-3,]),'>':([1,4,5,8,9,10,],[-5,7,7,-4,-2,-3,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,2,6,7,],[4,5,9,10,]),'statement':([0,],[3,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> expression','statement',1,'p_statement_expr','composition_calc.py',45),
  ('expression -> expression + expression','expression',3,'p_expression_binop','composition_calc.py',50),
  ('expression -> expression > expression','expression',3,'p_expression_binop','composition_calc.py',51),
  ('expression -> ( expression )','expression',3,'p_expression_group','composition_calc.py',61),
  ('expression -> NAME','expression',1,'p_expression_name','composition_calc.py',66),
]
