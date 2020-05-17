# Scheme Interpreter in Python

# I am changing this from Peter Norvig, 2010-16, http://norvig.com/lispy.html

from __future__ import division
import math
import operator as op
import datetime
import types
import sys

sys.setrecursionlimit(4000)

Bool = bool
String = str          			# A Lisp String is implemented as a Python str
Number = (int, float) 	        # A Lisp Number is implemented as a Python int or float
# List中可以包含List、Number、String、Bool
List   = list         			# A Lisp List is implemented as a Python list
Tuple  = tuple
Dict   = dict
    

isa = isinstance

# env中有两个变量，其中my存放 [块/函数] 计算时新定义的变量；father指向上层环境变量。
# 查找变量时，必须沿着叶子节点my一直找到根（None）。
class env:
    def __init__(self, fa):
        # my中的一项是一对key-value：“i”:[12, 0]，其中value的第一项是变量值，第二项0表示未使用，1表示已经使用. 
        self.my = {}
        self.father = fa

# 查查var变量，返回var所在的e
def find(var, e):
    if var in list(e.my.keys()):
        return e
    else:
        e = e.father
        while e != None:
            if var in e.my.keys():
                return e
            else:
                e = e.father
        return None
        
env_g = env(None);

# callcc函数里定义一个throw函数, throw作为proc的参数

def callcc(proc):
    "Call proc with current continuation; escape only"
    ball = RuntimeWarning("Sorry, can't continue this continuation any longer.")
    def throw(retval): 
        ball.retval = retval; 
        raise ball
    try:
        return proc(throw)
    except RuntimeWarning as w:
        if w is ball: 
            #print(".... ", ball.retval)
            return ball.retval
        else: 
            raise w

# 环境变量（全局变量），用户可以修改。
env_g.my.update({
        '+':    op.add, 
        '-':    op.sub, 
        '*':    op.mul, 
        '/':    op.truediv, 
        '>':    op.gt, 
        '<':    op.lt, 
        '>=':   op.ge, 
        '<=':   op.le, 
        '=':    op.eq, 
		'not':     op.not_,
		'eq?':     op.is_, 
        'equal?':  op.eq, 
		'max':     max,
        'min':     min,
        'abs':     abs,
		'round':   round,
        
        'tuple':   lambda *x: tuple(x),
        'dict':    lambda x: dict(x),
        
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'list':    lambda *x: list(x), 
        # 考虑用[]实现列表下标
        'list-ref':lambda x, y: x[y], 
		
        'append':  op.add,  	# 连接两个列表
		'len':     len, 		# 列表长度
		'map':     map,
		'print':   print,
		'exit':	   exit,
        
        'open':    open,
                
        'call/cc': callcc,
        
        'procedure?': callable,
        'null?':   lambda x: x == [], 
        # python的bool可能有错 bool("False")返回了True
        'bool?':   lambda x: isa(x, Bool),   
		'number?': lambda x: isa(x, Number),   
        'string?': lambda x: isa(x, String),
        'tuple?':  lambda x: isa(x, Tuple), 
		'list?':   lambda x: isa(x, List), 
        'dict?':   lambda x: isa(x, Dict),
        
        'not':     lambda x: not(x),
        'and':     lambda x, y: x and y,
        'or':      lambda x: x or y,
        
        'isa':     isinstance,
        
        'dir':     dir,
        'type':    type,
        'getattr': getattr,
        'setattr': setattr,
        '.':       lambda x, y: getattr(x, y), 
        
        'int': {}
})

env_g.my.update(vars(math)) # sin, cos, sqrt, pi, ...
       
b = RuntimeWarning("Return ...")
       
def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        repl()
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
	    # 这里将字符串转成具体的数据类型，
        return atom(token)

def atom(token):
	# 注意，转换次序。
    try: 
        return int(token)
    except ValueError:
        try: 
            return float(token)
        except ValueError:
            if token == "True":
                return True
            if token == "False":
                return False
            else:
                return String(token)

# call this to entery Interaction.

def repl(prompt='ZhScheme> '):
    "A prompt-read-eval-print loop."
    while True:
        # 读取输入，并解析，得到字符串列表
        tmp = parse(input(prompt))
        print(tmp)
        
        # 分析列表的意义，并计算。
        val = eval(tmp, env_g)
        
        # 打印计算结果
        if val is not None: 
            print(val)
            #print(lispstr(val))

def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, List):
        return '(' + ' '.join(map(lispstr, exp)) + ')' 
    else:
        return str(exp)

# 函数可能有返回值，也可能返回None，也就是没有返回值。
class Procedure(object):

    def __init__(self, parms, body, e):
        self.parms, self.body, self.e = parms, body, e
        
    def __call__(self, *args): 
    
        # parms是形参，args是实参
        for i in range(len(self.parms)):
            self.e.my[self.parms[i]] = args[i]
        
        # 如果实参是变量，则变量对应的值（列表）第二项置为1，表示已被使用。
        if isa(args[i], String):
            e0 = find(args[i], e)
            if e0 != None:
                e0[args[i]][1] = 1
                        
        try:
            return eval(self.body, self.e)
        except RuntimeWarning as w:
            if w is b: 
                return b.retval
 
# x： 待解析的list
# e:  env对象

# 可能返回一个bool,int,float,string,list或者None

def eval(x, e):
    
    if isa(x, List):
        if x == []:
            return
                
        # 哪些是全局过程，哪些是关键字？
        # 如果希望利用Python内置过程，则放进env_g里。
        
        # 用于注释
        elif x[0] == 'quote':
            return
            
        # 打印当前的环境。
        if x[0] == 'env':
        
            print("variables ...\n")
            for i in e.my.keys():
                print(i, " : ", e.my[i])
            
            return;
            
        elif x[0] == 'time':
        
            start = datetime.datetime.now()
            eval(x[1], e)
            end = datetime.datetime.now()    
            print(end - start)
         
        # type/racket
        # 整型变量 (int a) (int a 3)
        elif x[0] == 'int':
            return
            
        # 动态变量
        elif x[0] == 'define':       
            # 定义函数
            if isa(x[1], List):
                if x[1][0] not in e.my.keys():
                    # 函数体内定义的变量，存在c.my中，只在函数内可见。
                    c = env(e)
                    e.my[x[1][0]] = [Procedure(x[1][1:], x[2], c), 0]    
                return
                
            # 定义变量
            if x[1] not in e.my.keys():
                e.my[x[1]] = [eval(x[2], e), 0]
            else:
                print("Error : define [" + x[1] + "] again.")
            return
            
        elif x[0] == 'set':                
            # 为变量赋值
            if x[1] in e.my.keys():
                e.my[x[1]] = [eval(x[2], e), 1]
            else:
                print("Error : [" + x[1] + "] not define.")
            return
            
        # (set-list x 2 12)   设置列表的某一项       
        elif x[0] == 'set-list':
            if len(x) != 4:
                print("Error : [set-list] need 4 args.")
                return
            
            a = eval(x[1], e)
            b = eval(x[2], e)
            c = eval(x[3], e)
            
            if isa(a, List):
                a[b] = c
            else:
                print("Error : argument 1 must be a list.")
            return
                
        # (begin (...) (...) (...)) 依次执行，返回最后一项的运算结果。
        elif x[0] == 'begin':
            l = len(x)
            for i in range(l - 1):
                if i != l - 2:
                    eval(x[i+1], e)
            # 返回最后一项
            return eval(x[i+1], e)

        elif x[0] == 'lambda':
        
            # (define a (lambda x (print x)))
            # (lambda parms body)
            if len(x) != 3:
                print("Error : [lambda] needs 2 args.")
                return 
            return Procedure(x[1], x[2], e)
            
        elif x[0] == 'if':        
            cond = eval(x[1], e)
            if cond == True:
                return eval(x[2], e)
            else:
                if len(x) == 4:
                    return eval(x[3], e)
            return

        elif x[0] == 'switch':
            return
     
        elif x[0] == 'while':
        
            if (len(x) != 3):
                print("Error : [while] needs 2 args.")
                
            while eval(x[1], e):
                # 检测到break，很可能是跳出循环。
                if eval(x[2], e) == 'break':
                    break
            return
            
        elif x[0] == 'for':
        
            if (len(x) != 5):
                print("Error : [for] needs 4 args.")
                
            eval(x[1], e)
            while True:
                if eval(x[2], e) == True:
                    tmp = eval(x[4], e)
                    if tmp == 'break':
                        break
                else:
                    break
                eval(x[3], e)     # (+ i 1) 步长
                
            return
        
        # 定义类以及数据成员(class point (list (list n 2)(list m (lambda x (* 2 x)))))
        elif x[0] == 'class':
        
            print(x[2])
            tmp = type(x[1],(object,),dict(eval(x[2], e)))
            dir(tmp)
            if x[1] not in e.my.keys():
                e.my[x[1]] = tmp
            else:
                print("Error : define [" + x[1] + "] again.")
            return
            
        elif x[0] == 'break':
            return 'break'
            
        # ??? 函数返回，用try,except实现。
        # 用call/cc
        elif x[0] == 'return':
            b.retval = eval(x[1], e)
            raise b
            
        else:                       
            e0 = find(x[0], e)
            
            #使用改变量之前，将变量对应的列表第二项置为1
            if isa(e0.my[x[0]], List):
                e0.my[x[0]][1] = 1
                tmp = e0.my[x[0]][0]
            else:
                # 内置函数
                tmp = e0.my[x[0]]

            # 函数调用
            if callable(tmp):
                args = []
                for i in x[1:]:
                    args = args + [eval(i, e)]
                return tmp(*args)
                
            if type(tmp) is types.new_class: 
                # (point) 创造对象
                return tmp()
            
    if isa(x, String):
        #如果x在环境变量里，那么很可能是一个变量，而不是字符串。
        e0 = find(x, e)
        if e0 != None:
            if isa(e0.my[x], List):
                # 此处表明是用户定义变量，而不是内置变量。
                e0.my[x][1] = 1
                return e0.my[x][0]
            return e0.my[x]
        else:
            return x
            
    return x   

if len(sys.argv) == 1:
    # 逐行解释执行用户输入
    repl()
    exit()

def is_blank(line):
    for ch in line:
        if ch != ' ' and ch != '\t' and ch != '\n' and ch != '\r':
            return False
    return True

# 传入tokens不能为空列表
def get_list(tokens):
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(get_list(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('Error Message: Unexpected [)]')
    else:
	    # 这里将字符串转成具体的数据类型，
        return atom(token)
        
# 以行为单位读取文件并解释执行。
def eval_as_line(f):
    for line in f:
        if is_blank(line):
            continue
        
        print("...>")
        print(line)
        # 分析列表的意义，并计算。
        val = eval(parse(line), env_g)
        
        # 打印计算结果
        if val is not None: 
            print(val)
          
def eval_as_file(f):
    tmp = get_list(tokenize(f.read()))
    #print(tmp)    
    eval(tmp, env_g)

if len(sys.argv) == 2:
    f = open(sys.argv[1], "r")
    
    #eval_as_line(f)
    eval_as_file(f)
        
    f.close()
    
    for i in env_g.my.keys():
        if isa(env_g.my[i] ,List) and env_g.my[i][1] == 0:
            print("Warn : [", i, "] is not used." )
    exit()