
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightUPLUSUMINUSAND ARROW ASSIGN BEGIN BOOL_LITERAL BREAK COLOR_LITERAL COMMA COND COND_ELSE CONTINUE DEFINE DELIM DIV END EQ FLOAT_LITERAL FOR_STMT FOR_STMT_BY FOR_STMT_TO GE GT ID IF_COND IF_COND_ELSE INT_LITERAL LE LPAR LSQBR LT MINUS MOD MUL NEQ NOT OR PLUS RPAR RSQBR STR_LITERALstatement_list :\n                      | statement\n                      | statement_list statementstatement : fun_def_stmt\n                 | expression_stmt\n                 | loop_break_stmt\n                 | loop_continue_stmtloop_break_stmt : BREAK DELIMloop_continue_stmt : CONTINUE DELIMexpression_stmt : simple_expression DELIM\n                       | complex_expression\n                       | var_def_stmt\n                       | var_defs_stmt\n                       | var_assign_stmtvar_assign_stmt : ID ASSIGN expression DELIMvar_def_stmt : var_def DELIM\n                    | var_def COMMA\n                    | var_def2var_def : ID DEFINE simple_expressionvar_def2 : ID DEFINE complex_expressionvar_defs_stmt : LSQBR id_list RSQBR DEFINE LSQBR simple_expr_list RSQBR DELIMid_list : ID\n               | id_list COMMA IDexpression : simple_expression\n                  | complex_expressionsimple_expr_list : simple_expression\n                        | simple_expr_list COMMA simple_expression\n                        | id_list\n                        | id_list COMMA simple_expressionsimple_expression : or_expr\n                         | or_expr COND simple_expression COND_ELSE simple_expressionor_expr : and_expr\n               | or_expr OR and_exprand_expr : eq_expr\n                | and_expr AND eq_expreq_expr : cmp_expr\n               | cmp_expr EQ cmp_expr\n               | cmp_expr NEQ cmp_exprcmp_expr : add_expr\n                | add_expr GT add_expr\n                | add_expr GE add_expr\n                | add_expr LT add_expr\n                | add_expr LE add_expradd_expr : mul_expr\n                | add_expr PLUS mul_expr\n                | add_expr MINUS mul_exprmul_expr : unary_expr\n                | mul_expr MUL unary_expr\n                | mul_expr DIV unary_expr\n                | mul_expr MOD unary_exprunary_expr : sqbr_expr\n                  | NOT sqbr_expr\n                  | PLUS sqbr_expr %prec UPLUS\n                  | MINUS sqbr_expr %prec UMINUSsqbr_expr : atom\n                 | atom LSQBR simple_expression RSQBRatom : fun_call\n            | var_ref\n            | literal\n            | LPAR simple_expression RPARvar_ref : IDfun_call : fun_call0\n                | fun_call1\n                | fun_call2\n                | fun_call3\n                | fun_call4\n                | fun_call5fun_call0 : ID LPAR RPARfun_call1 : ID LPAR id_list RPARfun_call2 : ID LPAR simple_expr_list RPARfun_call3 : ID LPAR kw_arg_list RPARfun_call4 : ID LPAR id_list COMMA kw_arg_list RPARfun_call5 : ID LPAR simple_expr_list COMMA kw_arg_list RPARkw_arg_list : kw_arg\n                   | kw_arg_list COMMA kw_argkw_arg : ID DEFINE simple_expressionliteral : INT_LITERAL\n               | FLOAT_LITERAL\n               | STR_LITERAL\n               | BOOL_LITERAL\n               | COLOR_LITERAL\n               | list_literallist_literal : LSQBR simple_expr_list RSQBRcomplex_expression : if_expr\n                          | for_exprif_expr : IF_COND simple_expression stmts_block\n               | IF_COND simple_expression stmts_block IF_COND_ELSE stmts_blockfor_expr : FOR_STMT var_def FOR_STMT_TO simple_expression stmts_block\n                | FOR_STMT var_def FOR_STMT_TO simple_expression FOR_STMT_BYstmts_block : BEGIN statement_list ENDfun_def_stmt : fun_def_stmt_1\n                    | fun_def_stmt_mfun_def_stmt_1 : ID LPAR id_list RPAR ARROW simple_expression DELIMfun_def_stmt_m : ID LPAR id_list RPAR ARROW stmts_block'
    
_lr_action_items = {'BREAK':([0,1,2,3,4,5,6,7,8,10,11,12,13,19,20,22,52,53,54,55,64,65,99,110,111,133,142,156,157,158,159,161,165,167,],[14,14,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,-84,-85,-18,-3,-10,-8,-9,-16,-17,-20,-86,14,-15,14,-87,-90,-88,-89,-94,-93,-21,]),'CONTINUE':([0,1,2,3,4,5,6,7,8,10,11,12,13,19,20,22,52,53,54,55,64,65,99,110,111,133,142,156,157,158,159,161,165,167,],[15,15,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,-84,-85,-18,-3,-10,-8,-9,-16,-17,-20,-86,15,-15,15,-87,-90,-88,-89,-94,-93,-21,]),'ID':([0,1,2,3,4,5,6,7,8,10,11,12,13,17,19,20,22,23,25,26,31,32,35,52,53,54,55,56,57,58,60,62,63,64,65,70,74,75,76,77,78,79,80,81,82,83,84,88,99,102,106,108,110,111,112,113,126,128,130,132,133,134,136,142,146,155,156,157,158,159,161,165,167,],[16,16,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,61,-84,-85,-18,68,61,73,61,61,61,-3,-10,-8,-9,89,61,61,68,61,61,-16,-17,61,61,61,61,61,61,61,61,61,61,61,61,61,-20,89,138,61,-86,16,61,61,61,147,149,152,-15,138,61,16,61,68,-87,-90,-88,-89,-94,-93,-21,]),'LSQBR':([0,1,2,3,4,5,6,7,8,10,11,12,13,16,17,19,20,22,23,25,31,32,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,63,64,65,68,70,74,75,76,77,78,79,80,81,82,83,84,88,89,91,99,100,102,106,107,108,110,111,112,113,126,127,128,129,130,131,133,134,136,137,138,142,146,147,149,153,155,156,157,158,159,161,162,163,165,167,],[23,23,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,-61,60,-84,-85,-18,60,60,60,60,60,88,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-3,-10,-8,-9,60,60,60,60,-61,60,60,-16,-17,-61,60,60,60,60,60,60,60,60,60,60,60,60,60,-61,-68,-20,-60,60,60,-83,60,-86,23,60,60,60,-69,60,-70,60,-71,-15,60,60,155,-61,23,60,-61,-61,-69,60,-87,-90,-88,-89,-94,-72,-73,-93,-21,]),'IF_COND':([0,1,2,3,4,5,6,7,8,10,11,12,13,19,20,22,52,53,54,55,57,58,64,65,99,110,111,133,142,156,157,158,159,161,165,167,],[25,25,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,-84,-85,-18,-3,-10,-8,-9,25,25,-16,-17,-20,-86,25,-15,25,-87,-90,-88,-89,-94,-93,-21,]),'FOR_STMT':([0,1,2,3,4,5,6,7,8,10,11,12,13,19,20,22,52,53,54,55,57,58,64,65,99,110,111,133,142,156,157,158,159,161,165,167,],[26,26,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,-84,-85,-18,-3,-10,-8,-9,26,26,-16,-17,-20,-86,26,-15,26,-87,-90,-88,-89,-94,-93,-21,]),'NOT':([0,1,2,3,4,5,6,7,8,10,11,12,13,17,19,20,22,23,25,52,53,54,55,56,57,58,60,62,63,64,65,70,74,75,76,77,78,79,80,81,82,83,84,88,99,102,106,108,110,111,112,113,126,128,130,133,134,136,142,146,155,156,157,158,159,161,165,167,],[35,35,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,35,-84,-85,-18,35,35,-3,-10,-8,-9,35,35,35,35,35,35,-16,-17,35,35,35,35,35,35,35,35,35,35,35,35,35,-20,35,35,35,-86,35,35,35,35,35,35,-15,35,35,35,35,35,-87,-90,-88,-89,-94,-93,-21,]),'PLUS':([0,1,2,3,4,5,6,7,8,10,11,12,13,16,17,19,20,22,23,25,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,63,64,65,68,70,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,91,99,100,102,106,107,108,110,111,112,113,116,117,118,119,120,121,122,123,124,126,127,128,129,130,131,133,134,136,138,142,144,146,147,149,153,155,156,157,158,159,161,162,163,165,167,],[31,31,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,-61,31,-84,-85,-18,31,31,80,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-3,-10,-8,-9,31,31,31,31,-61,31,31,-16,-17,-61,31,31,31,31,31,31,31,31,31,31,31,31,-53,-54,-52,31,-61,-68,-20,-60,31,31,-83,31,-86,31,31,31,80,80,80,80,-45,-46,-48,-49,-50,31,-69,31,-70,31,-71,-15,31,31,-61,31,-56,31,-61,-61,-69,31,-87,-90,-88,-89,-94,-72,-73,-93,-21,]),'MINUS':([0,1,2,3,4,5,6,7,8,10,11,12,13,16,17,19,20,22,23,25,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,63,64,65,68,70,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,91,99,100,102,106,107,108,110,111,112,113,116,117,118,119,120,121,122,123,124,126,127,128,129,130,131,133,134,136,138,142,144,146,147,149,153,155,156,157,158,159,161,162,163,165,167,],[32,32,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,-61,32,-84,-85,-18,32,32,81,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-3,-10,-8,-9,32,32,32,32,-61,32,32,-16,-17,-61,32,32,32,32,32,32,32,32,32,32,32,32,-53,-54,-52,32,-61,-68,-20,-60,32,32,-83,32,-86,32,32,32,81,81,81,81,-45,-46,-48,-49,-50,32,-69,32,-70,32,-71,-15,32,32,-61,32,-56,32,-61,-61,-69,32,-87,-90,-88,-89,-94,-72,-73,-93,-21,]),'LPAR':([0,1,2,3,4,5,6,7,8,10,11,12,13,16,17,19,20,22,23,25,31,32,35,52,53,54,55,56,57,58,60,61,62,63,64,65,68,70,74,75,76,77,78,79,80,81,82,83,84,88,89,99,102,106,108,110,111,112,113,126,128,130,133,134,136,138,142,146,147,149,155,156,157,158,159,161,165,167,],[17,17,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,56,17,-84,-85,-18,17,17,17,17,17,-3,-10,-8,-9,17,17,17,17,102,17,17,-16,-17,102,17,17,17,17,17,17,17,17,17,17,17,17,17,102,-20,17,17,17,-86,17,17,17,17,17,17,-15,17,17,102,17,17,102,102,17,-87,-90,-88,-89,-94,-93,-21,]),'INT_LITERAL':([0,1,2,3,4,5,6,7,8,10,11,12,13,17,19,20,22,23,25,31,32,35,52,53,54,55,56,57,58,60,62,63,64,65,70,74,75,76,77,78,79,80,81,82,83,84,88,99,102,106,108,110,111,112,113,126,128,130,133,134,136,142,146,155,156,157,158,159,161,165,167,],[46,46,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,46,-84,-85,-18,46,46,46,46,46,-3,-10,-8,-9,46,46,46,46,46,46,-16,-17,46,46,46,46,46,46,46,46,46,46,46,46,46,-20,46,46,46,-86,46,46,46,46,46,46,-15,46,46,46,46,46,-87,-90,-88,-89,-94,-93,-21,]),'FLOAT_LITERAL':([0,1,2,3,4,5,6,7,8,10,11,12,13,17,19,20,22,23,25,31,32,35,52,53,54,55,56,57,58,60,62,63,64,65,70,74,75,76,77,78,79,80,81,82,83,84,88,99,102,106,108,110,111,112,113,126,128,130,133,134,136,142,146,155,156,157,158,159,161,165,167,],[47,47,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,47,-84,-85,-18,47,47,47,47,47,-3,-10,-8,-9,47,47,47,47,47,47,-16,-17,47,47,47,47,47,47,47,47,47,47,47,47,47,-20,47,47,47,-86,47,47,47,47,47,47,-15,47,47,47,47,47,-87,-90,-88,-89,-94,-93,-21,]),'STR_LITERAL':([0,1,2,3,4,5,6,7,8,10,11,12,13,17,19,20,22,23,25,31,32,35,52,53,54,55,56,57,58,60,62,63,64,65,70,74,75,76,77,78,79,80,81,82,83,84,88,99,102,106,108,110,111,112,113,126,128,130,133,134,136,142,146,155,156,157,158,159,161,165,167,],[48,48,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,48,-84,-85,-18,48,48,48,48,48,-3,-10,-8,-9,48,48,48,48,48,48,-16,-17,48,48,48,48,48,48,48,48,48,48,48,48,48,-20,48,48,48,-86,48,48,48,48,48,48,-15,48,48,48,48,48,-87,-90,-88,-89,-94,-93,-21,]),'BOOL_LITERAL':([0,1,2,3,4,5,6,7,8,10,11,12,13,17,19,20,22,23,25,31,32,35,52,53,54,55,56,57,58,60,62,63,64,65,70,74,75,76,77,78,79,80,81,82,83,84,88,99,102,106,108,110,111,112,113,126,128,130,133,134,136,142,146,155,156,157,158,159,161,165,167,],[49,49,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,49,-84,-85,-18,49,49,49,49,49,-3,-10,-8,-9,49,49,49,49,49,49,-16,-17,49,49,49,49,49,49,49,49,49,49,49,49,49,-20,49,49,49,-86,49,49,49,49,49,49,-15,49,49,49,49,49,-87,-90,-88,-89,-94,-93,-21,]),'COLOR_LITERAL':([0,1,2,3,4,5,6,7,8,10,11,12,13,17,19,20,22,23,25,31,32,35,52,53,54,55,56,57,58,60,62,63,64,65,70,74,75,76,77,78,79,80,81,82,83,84,88,99,102,106,108,110,111,112,113,126,128,130,133,134,136,142,146,155,156,157,158,159,161,165,167,],[50,50,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,50,-84,-85,-18,50,50,50,50,50,-3,-10,-8,-9,50,50,50,50,50,50,-16,-17,50,50,50,50,50,50,50,50,50,50,50,50,50,-20,50,50,50,-86,50,50,50,50,50,50,-15,50,50,50,50,50,-87,-90,-88,-89,-94,-93,-21,]),'$end':([0,1,2,3,4,5,6,7,8,10,11,12,13,19,20,22,52,53,54,55,64,65,99,110,133,156,157,158,159,161,165,167,],[-1,0,-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,-84,-85,-18,-3,-10,-8,-9,-16,-17,-20,-86,-15,-87,-90,-88,-89,-94,-93,-21,]),'END':([2,3,4,5,6,7,8,10,11,12,13,19,20,22,52,53,54,55,64,65,99,110,111,133,142,156,157,158,159,161,165,167,],[-2,-4,-5,-6,-7,-91,-92,-11,-12,-13,-14,-84,-85,-18,-3,-10,-8,-9,-16,-17,-20,-86,-1,-15,157,-87,-90,-88,-89,-94,-93,-21,]),'DELIM':([9,14,15,16,18,19,20,21,24,27,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,85,86,87,91,95,96,97,98,100,104,107,109,110,114,115,116,117,118,119,120,121,122,123,124,127,129,131,144,153,154,156,157,158,159,160,162,163,166,],[53,54,55,-61,-30,-84,-85,64,-32,-34,-36,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-53,-54,-52,-68,133,-24,-25,-19,-60,-33,-83,-35,-86,-37,-38,-40,-41,-42,-43,-45,-46,-48,-49,-50,-69,-70,-71,-56,-69,-31,-87,-90,-88,-89,165,-72,-73,167,]),'ASSIGN':([16,],[57,]),'DEFINE':([16,73,89,105,147,149,152,],[58,113,126,137,126,126,126,]),'MUL':([16,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,68,85,86,87,89,91,100,107,120,121,122,123,124,127,129,131,138,144,147,149,153,162,163,],[-61,82,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-61,-53,-54,-52,-61,-68,-60,-83,82,82,-48,-49,-50,-69,-70,-71,-61,-56,-61,-61,-69,-72,-73,]),'DIV':([16,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,68,85,86,87,89,91,100,107,120,121,122,123,124,127,129,131,138,144,147,149,153,162,163,],[-61,83,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-61,-53,-54,-52,-61,-68,-60,-83,83,83,-48,-49,-50,-69,-70,-71,-61,-56,-61,-61,-69,-72,-73,]),'MOD':([16,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,68,85,86,87,89,91,100,107,120,121,122,123,124,127,129,131,138,144,147,149,153,162,163,],[-61,84,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-61,-53,-54,-52,-61,-68,-60,-83,84,84,-48,-49,-50,-69,-70,-71,-61,-56,-61,-61,-69,-72,-73,]),'GT':([16,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,68,85,86,87,89,91,100,107,120,121,122,123,124,127,129,131,138,144,147,149,153,162,163,],[-61,76,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-61,-53,-54,-52,-61,-68,-60,-83,-45,-46,-48,-49,-50,-69,-70,-71,-61,-56,-61,-61,-69,-72,-73,]),'GE':([16,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,68,85,86,87,89,91,100,107,120,121,122,123,124,127,129,131,138,144,147,149,153,162,163,],[-61,77,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-61,-53,-54,-52,-61,-68,-60,-83,-45,-46,-48,-49,-50,-69,-70,-71,-61,-56,-61,-61,-69,-72,-73,]),'LT':([16,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,68,85,86,87,89,91,100,107,120,121,122,123,124,127,129,131,138,144,147,149,153,162,163,],[-61,78,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-61,-53,-54,-52,-61,-68,-60,-83,-45,-46,-48,-49,-50,-69,-70,-71,-61,-56,-61,-61,-69,-72,-73,]),'LE':([16,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,68,85,86,87,89,91,100,107,120,121,122,123,124,127,129,131,138,144,147,149,153,162,163,],[-61,79,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-61,-53,-54,-52,-61,-68,-60,-83,-45,-46,-48,-49,-50,-69,-70,-71,-61,-56,-61,-61,-69,-72,-73,]),'EQ':([16,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,68,85,86,87,89,91,100,107,116,117,118,119,120,121,122,123,124,127,129,131,138,144,147,149,153,162,163,],[-61,74,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-61,-53,-54,-52,-61,-68,-60,-83,-40,-41,-42,-43,-45,-46,-48,-49,-50,-69,-70,-71,-61,-56,-61,-61,-69,-72,-73,]),'NEQ':([16,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,68,85,86,87,89,91,100,107,116,117,118,119,120,121,122,123,124,127,129,131,138,144,147,149,153,162,163,],[-61,75,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-61,-53,-54,-52,-61,-68,-60,-83,-40,-41,-42,-43,-45,-46,-48,-49,-50,-69,-70,-71,-61,-56,-61,-61,-69,-72,-73,]),'AND':([16,24,27,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,68,85,86,87,89,91,100,104,107,109,114,115,116,117,118,119,120,121,122,123,124,127,129,131,138,144,147,149,153,162,163,],[-61,70,-34,-36,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-61,-53,-54,-52,-61,-68,-60,70,-83,-35,-37,-38,-40,-41,-42,-43,-45,-46,-48,-49,-50,-69,-70,-71,-61,-56,-61,-61,-69,-72,-73,]),'COND':([16,18,24,27,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,68,85,86,87,89,91,100,104,107,109,114,115,116,117,118,119,120,121,122,123,124,127,129,131,138,144,147,149,153,162,163,],[-61,62,-32,-34,-36,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-61,-53,-54,-52,-61,-68,-60,-33,-83,-35,-37,-38,-40,-41,-42,-43,-45,-46,-48,-49,-50,-69,-70,-71,-61,-56,-61,-61,-69,-72,-73,]),'OR':([16,18,24,27,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,68,85,86,87,89,91,100,104,107,109,114,115,116,117,118,119,120,121,122,123,124,127,129,131,138,144,147,149,153,162,163,],[-61,63,-32,-34,-36,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-61,-53,-54,-52,-61,-68,-60,-33,-83,-35,-37,-38,-40,-41,-42,-43,-45,-46,-48,-49,-50,-69,-70,-71,-61,-56,-61,-61,-69,-72,-73,]),'RPAR':([18,24,27,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,56,59,61,69,85,86,87,89,90,91,92,93,94,100,102,104,107,109,114,115,116,117,118,119,120,121,122,123,124,129,131,135,139,140,144,145,147,148,149,150,151,153,154,162,163,],[-30,-32,-34,-36,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,91,100,-61,-26,-53,-54,-52,-22,127,-68,129,131,-74,-60,91,-33,-83,-35,-37,-38,-40,-41,-42,-43,-45,-46,-48,-49,-50,-70,-71,153,-29,-27,-56,-76,-23,162,-61,163,-75,-69,-31,-72,-73,]),'RSQBR':([18,24,27,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,66,67,68,69,85,86,87,91,100,101,104,107,109,114,115,116,117,118,119,120,121,122,123,124,125,129,131,138,139,140,144,153,154,162,163,164,],[-30,-32,-34,-36,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,105,107,-22,-26,-53,-54,-52,-68,-60,-28,-33,-83,-35,-37,-38,-40,-41,-42,-43,-45,-46,-48,-49,-50,144,-70,-71,-23,-29,-27,-56,-69,-31,-72,-73,166,]),'COMMA':([18,21,24,27,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,66,67,68,69,85,86,87,89,90,91,92,93,94,98,100,101,104,107,109,114,115,116,117,118,119,120,121,122,123,124,129,131,135,138,139,140,144,145,147,148,149,150,151,153,154,162,163,164,],[-30,65,-32,-34,-36,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,106,108,-22,-26,-53,-54,-52,-22,128,-68,130,132,-74,-19,-60,134,-33,-83,-35,-37,-38,-40,-41,-42,-43,-45,-46,-48,-49,-50,-70,-71,128,-23,-29,-27,-56,-76,-23,132,-61,132,-75,-69,-31,-72,-73,108,]),'BEGIN':([18,24,27,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,71,85,86,87,91,100,104,107,109,114,115,116,117,118,119,120,121,122,123,124,129,131,141,143,144,146,153,154,162,163,],[-30,-32,-34,-36,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,111,-53,-54,-52,-68,-60,-33,-83,-35,-37,-38,-40,-41,-42,-43,-45,-46,-48,-49,-50,-70,-71,111,111,-56,111,-69,-31,-72,-73,]),'COND_ELSE':([18,24,27,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,85,86,87,91,100,103,104,107,109,114,115,116,117,118,119,120,121,122,123,124,129,131,144,153,154,162,163,],[-30,-32,-34,-36,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-53,-54,-52,-68,-60,136,-33,-83,-35,-37,-38,-40,-41,-42,-43,-45,-46,-48,-49,-50,-70,-71,-56,-69,-31,-72,-73,]),'FOR_STMT_BY':([18,24,27,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,85,86,87,91,100,104,107,109,114,115,116,117,118,119,120,121,122,123,124,129,131,143,144,153,154,162,163,],[-30,-32,-34,-36,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,-53,-54,-52,-68,-60,-33,-83,-35,-37,-38,-40,-41,-42,-43,-45,-46,-48,-49,-50,-70,-71,159,-56,-69,-31,-72,-73,]),'FOR_STMT_TO':([18,24,27,28,29,30,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,61,72,85,86,87,91,98,100,104,107,109,114,115,116,117,118,119,120,121,122,123,124,129,131,144,153,154,162,163,],[-30,-32,-34,-36,-39,-44,-47,-51,-55,-57,-58,-59,-62,-63,-64,-65,-66,-67,-77,-78,-79,-80,-81,-82,-61,112,-53,-54,-52,-68,-19,-60,-33,-83,-35,-37,-38,-40,-41,-42,-43,-45,-46,-48,-49,-50,-70,-71,-56,-69,-31,-72,-73,]),'IF_COND_ELSE':([110,157,],[141,-90,]),'ARROW':([127,],[146,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement_list':([0,111,],[1,142,]),'statement':([0,1,111,142,],[2,52,2,52,]),'fun_def_stmt':([0,1,111,142,],[3,3,3,3,]),'expression_stmt':([0,1,111,142,],[4,4,4,4,]),'loop_break_stmt':([0,1,111,142,],[5,5,5,5,]),'loop_continue_stmt':([0,1,111,142,],[6,6,6,6,]),'fun_def_stmt_1':([0,1,111,142,],[7,7,7,7,]),'fun_def_stmt_m':([0,1,111,142,],[8,8,8,8,]),'simple_expression':([0,1,17,23,25,56,57,58,60,62,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[9,9,59,69,71,69,96,98,69,103,125,69,139,140,9,143,98,145,139,140,139,154,9,160,69,]),'complex_expression':([0,1,57,58,111,142,],[10,10,97,99,10,10,]),'var_def_stmt':([0,1,111,142,],[11,11,11,11,]),'var_defs_stmt':([0,1,111,142,],[12,12,12,12,]),'var_assign_stmt':([0,1,111,142,],[13,13,13,13,]),'or_expr':([0,1,17,23,25,56,57,58,60,62,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,]),'if_expr':([0,1,57,58,111,142,],[19,19,19,19,19,19,]),'for_expr':([0,1,57,58,111,142,],[20,20,20,20,20,20,]),'var_def':([0,1,26,111,142,],[21,21,72,21,21,]),'var_def2':([0,1,111,142,],[22,22,22,22,]),'and_expr':([0,1,17,23,25,56,57,58,60,62,63,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[24,24,24,24,24,24,24,24,24,24,104,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,]),'eq_expr':([0,1,17,23,25,56,57,58,60,62,63,70,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[27,27,27,27,27,27,27,27,27,27,27,109,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'cmp_expr':([0,1,17,23,25,56,57,58,60,62,63,70,74,75,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[28,28,28,28,28,28,28,28,28,28,28,28,114,115,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,]),'add_expr':([0,1,17,23,25,56,57,58,60,62,63,70,74,75,76,77,78,79,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[29,29,29,29,29,29,29,29,29,29,29,29,29,29,116,117,118,119,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,]),'mul_expr':([0,1,17,23,25,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,120,121,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,]),'unary_expr':([0,1,17,23,25,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,122,123,124,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,]),'sqbr_expr':([0,1,17,23,25,31,32,35,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[34,34,34,34,34,85,86,87,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'atom':([0,1,17,23,25,31,32,35,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,]),'fun_call':([0,1,17,23,25,31,32,35,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,]),'var_ref':([0,1,17,23,25,31,32,35,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,]),'literal':([0,1,17,23,25,31,32,35,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'fun_call0':([0,1,17,23,25,31,32,35,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,]),'fun_call1':([0,1,17,23,25,31,32,35,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,]),'fun_call2':([0,1,17,23,25,31,32,35,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,]),'fun_call3':([0,1,17,23,25,31,32,35,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,]),'fun_call4':([0,1,17,23,25,31,32,35,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,]),'fun_call5':([0,1,17,23,25,31,32,35,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,]),'list_literal':([0,1,17,23,25,31,32,35,56,57,58,60,62,63,70,74,75,76,77,78,79,80,81,82,83,84,88,102,106,108,111,112,113,126,128,130,134,136,142,146,155,],[51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,]),'id_list':([23,56,60,102,155,],[66,90,101,135,101,]),'simple_expr_list':([23,56,60,102,155,],[67,92,67,92,164,]),'kw_arg_list':([56,102,128,130,],[93,93,148,150,]),'kw_arg':([56,102,128,130,132,],[94,94,94,94,151,]),'expression':([57,],[95,]),'stmts_block':([71,141,143,146,],[110,156,158,161,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement_list","S'",1,None,None,None),
  ('statement_list -> <empty>','statement_list',0,'p_statement_list','parser.py',30),
  ('statement_list -> statement','statement_list',1,'p_statement_list','parser.py',31),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list','parser.py',32),
  ('statement -> fun_def_stmt','statement',1,'p_statement','parser.py',41),
  ('statement -> expression_stmt','statement',1,'p_statement','parser.py',42),
  ('statement -> loop_break_stmt','statement',1,'p_statement','parser.py',43),
  ('statement -> loop_continue_stmt','statement',1,'p_statement','parser.py',44),
  ('loop_break_stmt -> BREAK DELIM','loop_break_stmt',2,'p_loop_break_stmt','parser.py',49),
  ('loop_continue_stmt -> CONTINUE DELIM','loop_continue_stmt',2,'p_loop_continue_stmt','parser.py',53),
  ('expression_stmt -> simple_expression DELIM','expression_stmt',2,'p_expression_stmt','parser.py',58),
  ('expression_stmt -> complex_expression','expression_stmt',1,'p_expression_stmt','parser.py',59),
  ('expression_stmt -> var_def_stmt','expression_stmt',1,'p_expression_stmt','parser.py',60),
  ('expression_stmt -> var_defs_stmt','expression_stmt',1,'p_expression_stmt','parser.py',61),
  ('expression_stmt -> var_assign_stmt','expression_stmt',1,'p_expression_stmt','parser.py',62),
  ('var_assign_stmt -> ID ASSIGN expression DELIM','var_assign_stmt',4,'p_var_assign_stmt','parser.py',66),
  ('var_def_stmt -> var_def DELIM','var_def_stmt',2,'p_var_def_stmt1','parser.py',70),
  ('var_def_stmt -> var_def COMMA','var_def_stmt',2,'p_var_def_stmt1','parser.py',71),
  ('var_def_stmt -> var_def2','var_def_stmt',1,'p_var_def_stmt1','parser.py',72),
  ('var_def -> ID DEFINE simple_expression','var_def',3,'p_var_def','parser.py',76),
  ('var_def2 -> ID DEFINE complex_expression','var_def2',3,'p_var_def2','parser.py',80),
  ('var_defs_stmt -> LSQBR id_list RSQBR DEFINE LSQBR simple_expr_list RSQBR DELIM','var_defs_stmt',8,'p_var_defs_stmt','parser.py',84),
  ('id_list -> ID','id_list',1,'p_id_list','parser.py',88),
  ('id_list -> id_list COMMA ID','id_list',3,'p_id_list','parser.py',89),
  ('expression -> simple_expression','expression',1,'p_expression','parser.py',94),
  ('expression -> complex_expression','expression',1,'p_expression','parser.py',95),
  ('simple_expr_list -> simple_expression','simple_expr_list',1,'p_simple_expr_list','parser.py',100),
  ('simple_expr_list -> simple_expr_list COMMA simple_expression','simple_expr_list',3,'p_simple_expr_list','parser.py',101),
  ('simple_expr_list -> id_list','simple_expr_list',1,'p_simple_expr_list','parser.py',102),
  ('simple_expr_list -> id_list COMMA simple_expression','simple_expr_list',3,'p_simple_expr_list','parser.py',103),
  ('simple_expression -> or_expr','simple_expression',1,'p_simple_expression','parser.py',129),
  ('simple_expression -> or_expr COND simple_expression COND_ELSE simple_expression','simple_expression',5,'p_simple_expression','parser.py',130),
  ('or_expr -> and_expr','or_expr',1,'p_or_expr','parser.py',137),
  ('or_expr -> or_expr OR and_expr','or_expr',3,'p_or_expr','parser.py',138),
  ('and_expr -> eq_expr','and_expr',1,'p_and_expr','parser.py',142),
  ('and_expr -> and_expr AND eq_expr','and_expr',3,'p_and_expr','parser.py',143),
  ('eq_expr -> cmp_expr','eq_expr',1,'p_eq_expr','parser.py',147),
  ('eq_expr -> cmp_expr EQ cmp_expr','eq_expr',3,'p_eq_expr','parser.py',148),
  ('eq_expr -> cmp_expr NEQ cmp_expr','eq_expr',3,'p_eq_expr','parser.py',149),
  ('cmp_expr -> add_expr','cmp_expr',1,'p_cmp_expr','parser.py',153),
  ('cmp_expr -> add_expr GT add_expr','cmp_expr',3,'p_cmp_expr','parser.py',154),
  ('cmp_expr -> add_expr GE add_expr','cmp_expr',3,'p_cmp_expr','parser.py',155),
  ('cmp_expr -> add_expr LT add_expr','cmp_expr',3,'p_cmp_expr','parser.py',156),
  ('cmp_expr -> add_expr LE add_expr','cmp_expr',3,'p_cmp_expr','parser.py',157),
  ('add_expr -> mul_expr','add_expr',1,'p_add_expr','parser.py',161),
  ('add_expr -> add_expr PLUS mul_expr','add_expr',3,'p_add_expr','parser.py',162),
  ('add_expr -> add_expr MINUS mul_expr','add_expr',3,'p_add_expr','parser.py',163),
  ('mul_expr -> unary_expr','mul_expr',1,'p_mul_expr','parser.py',167),
  ('mul_expr -> mul_expr MUL unary_expr','mul_expr',3,'p_mul_expr','parser.py',168),
  ('mul_expr -> mul_expr DIV unary_expr','mul_expr',3,'p_mul_expr','parser.py',169),
  ('mul_expr -> mul_expr MOD unary_expr','mul_expr',3,'p_mul_expr','parser.py',170),
  ('unary_expr -> sqbr_expr','unary_expr',1,'p_unary_expr','parser.py',177),
  ('unary_expr -> NOT sqbr_expr','unary_expr',2,'p_unary_expr','parser.py',178),
  ('unary_expr -> PLUS sqbr_expr','unary_expr',2,'p_unary_expr','parser.py',179),
  ('unary_expr -> MINUS sqbr_expr','unary_expr',2,'p_unary_expr','parser.py',180),
  ('sqbr_expr -> atom','sqbr_expr',1,'p_sqbr_expr','parser.py',187),
  ('sqbr_expr -> atom LSQBR simple_expression RSQBR','sqbr_expr',4,'p_sqbr_expr','parser.py',188),
  ('atom -> fun_call','atom',1,'p_atom','parser.py',192),
  ('atom -> var_ref','atom',1,'p_atom','parser.py',193),
  ('atom -> literal','atom',1,'p_atom','parser.py',194),
  ('atom -> LPAR simple_expression RPAR','atom',3,'p_atom','parser.py',195),
  ('var_ref -> ID','var_ref',1,'p_var_ref','parser.py',202),
  ('fun_call -> fun_call0','fun_call',1,'p_fun_call','parser.py',206),
  ('fun_call -> fun_call1','fun_call',1,'p_fun_call','parser.py',207),
  ('fun_call -> fun_call2','fun_call',1,'p_fun_call','parser.py',208),
  ('fun_call -> fun_call3','fun_call',1,'p_fun_call','parser.py',209),
  ('fun_call -> fun_call4','fun_call',1,'p_fun_call','parser.py',210),
  ('fun_call -> fun_call5','fun_call',1,'p_fun_call','parser.py',211),
  ('fun_call0 -> ID LPAR RPAR','fun_call0',3,'p_fun_call0','parser.py',224),
  ('fun_call1 -> ID LPAR id_list RPAR','fun_call1',4,'p_fun_call1','parser.py',228),
  ('fun_call2 -> ID LPAR simple_expr_list RPAR','fun_call2',4,'p_fun_call2','parser.py',232),
  ('fun_call3 -> ID LPAR kw_arg_list RPAR','fun_call3',4,'p_fun_call3','parser.py',236),
  ('fun_call4 -> ID LPAR id_list COMMA kw_arg_list RPAR','fun_call4',6,'p_fun_call4','parser.py',240),
  ('fun_call5 -> ID LPAR simple_expr_list COMMA kw_arg_list RPAR','fun_call5',6,'p_fun_call5','parser.py',244),
  ('kw_arg_list -> kw_arg','kw_arg_list',1,'p_kw_arg_list','parser.py',248),
  ('kw_arg_list -> kw_arg_list COMMA kw_arg','kw_arg_list',3,'p_kw_arg_list','parser.py',249),
  ('kw_arg -> ID DEFINE simple_expression','kw_arg',3,'p_kw_arg','parser.py',258),
  ('literal -> INT_LITERAL','literal',1,'p_literal','parser.py',262),
  ('literal -> FLOAT_LITERAL','literal',1,'p_literal','parser.py',263),
  ('literal -> STR_LITERAL','literal',1,'p_literal','parser.py',264),
  ('literal -> BOOL_LITERAL','literal',1,'p_literal','parser.py',265),
  ('literal -> COLOR_LITERAL','literal',1,'p_literal','parser.py',266),
  ('literal -> list_literal','literal',1,'p_literal','parser.py',267),
  ('list_literal -> LSQBR simple_expr_list RSQBR','list_literal',3,'p_list_leteral','parser.py',271),
  ('complex_expression -> if_expr','complex_expression',1,'p_complex_expression','parser.py',277),
  ('complex_expression -> for_expr','complex_expression',1,'p_complex_expression','parser.py',278),
  ('if_expr -> IF_COND simple_expression stmts_block','if_expr',3,'p_if_expr','parser.py',282),
  ('if_expr -> IF_COND simple_expression stmts_block IF_COND_ELSE stmts_block','if_expr',5,'p_if_expr','parser.py',283),
  ('for_expr -> FOR_STMT var_def FOR_STMT_TO simple_expression stmts_block','for_expr',5,'p_for_expr','parser.py',290),
  ('for_expr -> FOR_STMT var_def FOR_STMT_TO simple_expression FOR_STMT_BY','for_expr',5,'p_for_expr','parser.py',291),
  ('stmts_block -> BEGIN statement_list END','stmts_block',3,'p_stmts_block','parser.py',295),
  ('fun_def_stmt -> fun_def_stmt_1','fun_def_stmt',1,'p_fun_def_stmt','parser.py',301),
  ('fun_def_stmt -> fun_def_stmt_m','fun_def_stmt',1,'p_fun_def_stmt','parser.py',302),
  ('fun_def_stmt_1 -> ID LPAR id_list RPAR ARROW simple_expression DELIM','fun_def_stmt_1',7,'p_fun_def_stmt_1','parser.py',306),
  ('fun_def_stmt_m -> ID LPAR id_list RPAR ARROW stmts_block','fun_def_stmt_m',6,'p_fun_def_stmt_m','parser.py',310),
]
