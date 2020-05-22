# Scheme Interpreter in Python

# I am changing this from Peter Norvig, 2010-16, http://norvig.com/lispy.html

from __future__ import division
import math
import operator as op
import datetime
import types
import sys

sys.setrecursionlimit(1000000)

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

# 查找var变量，返回var所在的e
def find_all(var, e):
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
        
# 只在当前环境中查找var变量
def find(var, e):
    if var in list(e.my.keys()):
        return e
    else:
        return None
        
env_g = env(None);

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
        '[]':       lambda x, y: x[y], 
		
        'append':  op.add,  	# 连接两个列表
		'len':     len, 		# 列表长度
		'map':     map,
		'print':   print,
		'exit':	   exit,
        
        'open':    open,
                        
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
        '.' :      lambda x,y: getattr(x, y),
        'int': {}
})

env_g.my.update(vars(math)) # sin, cos, sqrt, pi, ...
              
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
            return String(token)
                
# call this to entery Interaction.

def repl(prompt='ZhScheme> '):
    "A prompt-read-eval_list-print loop."
    while True:
        # 读取输入，并解析，得到字符串列表
        tmp = parse(input(prompt))
        print(tmp)
        
        # 分析列表的意义，并计算。
        val = eval_list(tmp, env_g)
        
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

    def __init__(self, parms, body, e, type):
        self.parms, self.body, self.e, self.type = parms, body, e, type
        
    def __call__(self, *args): 
    
        # 函数体内定义的变量，存在c.my中，只在函数内可见。
        c = env(self.e)
    
        # parms是形参，args是实参
        for i in range(len(self.parms)):
            c.my[self.parms[i]] = args[i]

            #如果实参是变量，则变量对应的值（列表）第二项置为1，表示已被使用
            if isa(args[i], String) and self.type == "define":
                e0 = find_all(args[i], self.e)
                if e0 != None:
                    e0.my[args[i]][1] = 1
                        
        return eval_list(self.body, c)

# x： 待解析的list
# e:  env对象

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
        
# 可能返回一个bool,int,float,string,list或者None

def eval_list(x, e):
    
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
        
            print("env ...")
            for i in e.my.keys():
                print(i, " : ", e.my[i])
            print("....")
            return;
            
        elif x[0] == 'time':
        
            start = datetime.datetime.now()
            eval_list(x[1], e)
            end = datetime.datetime.now()    
            print(end - start)
         
        # type/racket
        # 整型变量 (int a) (int a 3)
        elif x[0] == 'int':
            return
            
        # 定义函数
        elif x[0] == 'define':       
            
            if isa(x[1], List):
                if x[1][0] not in e.my.keys():
                    e.my[x[1][0]] = [Procedure(x[1][1:], x[2], e, "define"), 0] 
                else:
                    print("Error: define [ ", x[1][0], " ] again.")
                    exit()
            else:
                print("Error: Should define a function.")
                exit()
            
        elif x[0] == 'set': 
            # (set (a b c) (2 3 44)) 一次定义/赋值多个变量
            if isa(x[1], List):
                pass
            else:
                # 往外层查找变量，是否定义过？
                tmp = find_all(x[1], e)
                # 为变量赋值
                if tmp != None:
                    tmp.my[x[1]] = [eval_list(x[2], e), 1]
                else:
                    # 首次定义
                    e.my[x[1]] = [eval_list(x[2], e), 0]
            return
            
        # (set-list x 2 12)   设置列表的某一项       
        elif x[0] == 'set-list':
            if len(x) != 4:
                print("Error : [set-list] need 4 args.")
                return
            
            a = eval_list(x[1], e)
            b = eval_list(x[2], e)
            c = eval_list(x[3], e)
            
            if isa(a, List):
                a[b] = c
            else:
                print("Error : argument 1 must be a list.")
            return

        elif x[0] == 'import':
            f = open(x[1], "r")            
            program = f.read()
            f.close()
            program = "(begin" + program + ")"
            tmp = get_list(tokenize(program))
            eval_list(tmp, e)

        # (begin (...) (...) (...)) 依次执行。
        elif x[0] == 'begin':
            l = len(x)
            for i in range(l - 1):
                if i + 1 == l - 1:
                    # 返回最后一项
                    return eval_list(x[i+1], e)
                else:
                    eval_list(x[i+1], e)

        elif x[0] == 'lambda':
        
            # (define a (lambda x (print x)))
            # (lambda parms body)
            if len(x) != 3:
                print("Error : [lambda] needs 2 args.")
                return 
            return Procedure(x[1], x[2], e, "lambda")
            
        elif x[0] == 'if':        
            cond = eval_list(x[1], e)
            if cond == True:
                return eval_list(x[2], e)
            else:
                if len(x) == 4:
                    return eval_list(x[3], e)
                    
        elif x[0] == 'while':
        
            if (len(x) != 3):
                print("Error : [while] needs 2 args.")
                
            while eval_list(x[1], e):
                # 检测到break，很可能是跳出循环。
                if eval_list(x[2], e) == 'break':
                    break
            return
            
        elif x[0] == 'for':
        
            if (len(x) != 5):
                print("Error : [for] needs 4 args.")
                
            eval_list(x[1], e)
            while True:
                if eval_list(x[2], e) == True:
                    tmp = eval_list(x[4], e)
                    if tmp == 'break':
                        break
                else:
                    break
                eval_list(x[3], e)     # (+ i 1) 步长
                
            return
            
        elif x[0] == 'for-each':
            for i in eval_list(x[2], e): 
                eval_list(x[1], e)(i)

        elif x[0] == 'class':
        
            print(x[2])
            tmp = type(x[1],(object,),dict(eval_list(x[2], e)))
            #dir(tmp)
            if x[1] not in e.my.keys():
                e.my[x[1]] = tmp
            else:
                print("Error : define [" + x[1] + "] again.")
            return
            
        elif x[0] == 'break':
            return 'break'      
            
        else:        
        
            tmp = eval_list(x[0], e)
            
            #对象函数调用
            if callable(tmp):
                args = []
                for i in x[1:]:
                    args = args + [eval_list(i, e)]
                return tmp(*args)

            e0 = find_all(x[0], e)
            
            if e0 == None:
                print("Error : What is [", x[0], "]?" )
                return 
                
            #使用参数之前，将参数变量对应的列表第二项置为1
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
                    args = args + [eval_list(i, e)]
                return tmp(*args)
                
            if type(tmp) is types.new_class: 
                # (point) 创造对象
                return tmp()
            
    if isa(x, String):
        if x == "True":
            return True
            
        if x == "False":
            return False
            
        #如果x在环境变量里，取其值。
        e0 = find_all(x, e)
        if e0 != None:
            # 判断该变量是用户定义变量，而不是内置变量。
            if isa(e0.my[x], List):
                e0.my[x][1] = 1
                return e0.my[x][0]
            return e0.my[x]
        
        # 第一个和最后一直字符都是"，表示是一个字符串。
        if x[0] == '\"' and x[-1] == '\"':
            return x[1:-1]
        
        # obj.he|1.o|2:-1  
        y = []
        z = x
        while True:
            for i in range(len(z)):
                if z[i] == '.' or z[i] == '|':
                    y = y + [z[0:i]] + [z[i]]
                    z = z[(i+1):]
                    break   
            else:
                break
        y = y + [z]                   
                     
        # y的长度为1，上面已经查找过环境变量，这里只能是字符串常量。
        if len(y) == 1:
            return x
            
        for i in range(len(y)):
            if i == 0:
                t = eval_list(y[0], e)
            #  对象成员
            if y[i] == '.':
                t = getattr(t, y[i+1])
            #  列表成员
            if y[i] == '|':
                t = t[int(y[i+1])]            
        return t
        
    # int float
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
        
# 以行为单位读取文件并解释执行。
def eval_as_line(f):
    for line in f:
        if is_blank(line):
            continue
        
        print("...>")
        print(line)
        # 分析列表的意义，并计算。
        val = eval_list(parse(line), env_g)
        
        # 打印计算结果
        if val is not None: 
            print(val)
          
def eval_file(f):
    program = f.read()
    program = "(begin" + program + ")"
    tmp = get_list(tokenize(program))
    eval_list(tmp, env_g)

if len(sys.argv) == 2:
    f = open(sys.argv[1], "r")
    
    #eval_as_line(f)
    eval_file(f)
        
    f.close()
    
    for i in env_g.my.keys():
        if isa(env_g.my[i] ,List) and env_g.my[i][1] == 0:
            print("Warn : [", i, "] is not used." )
    exit()