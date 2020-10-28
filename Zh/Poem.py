# Scheme Interpreter in Python

# I am changing this from Peter Norvig, 2010-16, http://norvig.com/lispy.html

from __future__ import division
import math
import operator as op
import datetime
import types
import sys
import os
import unittest
import tkinter

Bool = bool
String = str          			
Number = (int, float)

# List中可以包含List、Number、String、Bool、Tuple、Dict
List   = list        
Tuple  = tuple
Dict   = dict
    
isa = isinstance

class TailRecurseException(BaseException):
  def __init__(self, args, kwargs):
    self.args = args
    self.kwargs = kwargs

def tail_call_optimized(g):
  """
  This function decorates a function with tail call
  optimization. It does this by throwing an exception
  if it is it's own grandparent, and catching such
  exceptions to fake the tail call optimization.
  
  This function fails if the decorated
  function recurses in a non-tail context.
  """
  def func(*args, **kwargs):
    f = sys._getframe()
    if f.f_back and f.f_back.f_back \
        and f.f_back.f_back.f_code == f.f_code:
      print(args)
      #print(kwargs)
      #经测试，args为无默认值的参数对应的元组，kwargs为有默认值的参数对应的数组。
      raise TailRecurseException(args, kwargs)
    else:
      while 1:
        try:
          return g(*args, **kwargs)
        except TailRecurseException as e:
          args = e.args
          kwargs = e.kwargs
  func.__doc__ = g.__doc__
  return func

# env中有两个变量，其中my存放计算 [块/函数] 时定义的变量；father指向上层环境变量。
# 查找变量时，必须沿着叶子节点my一直找到根（None）。
class env:
    # def __init__(self, fa):
    def __init__(self, fa):
        # my中的一项是一对key-value：“i”:[12, 0]，
        # value的第一项是变量值，第二项0表示未使用，1表示已经使用. 
        self.my = {}
        self.father = fa

# 查找var变量，返回var所在的e
def find_all(var, e):
    if var in list(e.my.keys()):
        return e
    else:
        t = e.father
        while t != None:
            if var in t.my.keys():
                return t
            else:
                t = t.father
        return None
        
# 只在当前环境中查找var变量
def find(var, e):
    if var in list(e.my.keys()):
        return e
    else:
        return None

# (. sys (exit) (open)) 
def getatt(x, y):
    if isa(y, List):
        for i in y:
            i = getattr(x, i[0])
    if isa(y, Str):
        return getattr(x, y)
        
env_g = env(None)

# 环境变量（全局变量），用户自定义的全局变量和函数也保存在这里。
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
                
        # lambda *x 表示参数可能多于一个
        '\'':      lambda *x: list(x), 
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        
        'append':  op.add,  	# 连接两个列表
        'len':     len, 		# 列表长度
        'map':     map,
                                
        'null?':   lambda x: x == [],
        
        # python的bool可能有错 bool("False")返回了True
        'bool?':   lambda x: isa(x, Bool),   
        'number?': lambda x: isa(x, Number),   
        'string?': lambda x: isa(x, String),
        'tuple?':  lambda x: isa(x, Tuple), 
        'list?':   lambda x: isa(x, List), 
        'dict?':   lambda x: isa(x, Dict),
        
        'int':     int,
        'float':   float,
        
        'not':     lambda x: not(x),
        'and':     lambda x, y: x and y,
        'or':      lambda x: x or y,
        
        'isa':     isinstance,
        
        'dir':     dir,
        
        'getattr': getattr,
        'setattr': setattr,
        
        # 对象访问
        #'.' :      lambda x,y: getattr(x, y),          
        '.':        getatt,

        'object':   type(object()),
        'BaseException': BaseException,
        
        # 模块访问
        # '::':      lambda x,y: getattr(__import__(x), y),   
        
        # 字典key访问
        ':':       lambda x, y: x[y], 
})
        
env_g.my.update(vars(math)) # sin, cos, sqrt, pi, ...
#env_g.my.update(vars(os)) 

# 全局自定义变量/函数环境
en = env(env_g)

# 把Line中的双引号去掉，换成变量。
def YinHao(line):
    a = ""
    i=0
    for ch in line:
        if ch !=  "\"":
            a=a+ch
        else:
            pass
            
def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

# 返回的列表中各项已经判断了其数据类型。注意，怎么处理带空格的字符串？
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
        return atom(token)
        
# 判断字符串token的类型
def atom(token):
    try:
        return eval(token)
    except Exception:
        return token
        
# call this to entery Interaction.

def repl(prompt='Zh> '):
    "A prompt-read-eval_all-print loop."
    while True:
        # 读取输入，并解析，得到字符串列表
        tmp = parse(input(prompt))
        
        print(tmp)
        
        # 分析列表的意义，并计算。
        val = eval_all(tmp, en)
        
        # 打印计算结果
        if val is not None: 
            print(val)

def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, List):
        return '(' + ' '.join(map(lispstr, exp)) + ')' 
    else:
        return str(exp)

# 函数可能有返回值，也可能返回None，也就是没有返回值。
class Procedure(object):
    is_tail_recursion = False
    
    def __init__(self, name, parms, body, e):
        self.parms, self.body, self.e, self.name = parms, body, e, name
        l = len(body)
        
        # 最后一项函数调用和本函数名称一样，则是尾递归
        if isa(body[l-1],List):
            if body[l-1][0] == self.name:
                is_tail_recursion = True
            if body[l-1][0] == 'if':
                if l == 2:
                    if body[l-1][2] == name:
                        is_tail_recursion = True
                if l == 3:
                    if body[l-1][2] == name or body[l-1][3] == name:
                        is_tail_recursion = True
                        
    def __call__(self, *args): 
        # 函数体内定义的变量，存在c.my中，只在函数内可见。
        '''
        if self.is_tail_recursion == False:
            c = env(self.e)
        else:
            c = self.e
            '''
        c = env(self.e)

        # parms是形参，args是实参
        for i in range(len(self.parms)):
            c.my[self.parms[i]] = [args[i], 0]

            #如果实参是变量，则变量对应的值（列表）第二项置为1，表示已被使用
            if isa(args[i], String) and self.name != "lambda":
                e0 = find_all(args[i], self.e)
                if e0 != None:
                    e0.my[args[i]][1] = 1
        print(c.my)
        return eval_all(self.body, c)

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

def has_op(x):
    for i in x:
        if i == '.' or i == '|' or i == '+' or i == '-' or i == '*' or i == '/':
            return True
    return False
    
# "obj.he|1.o|2+2*3/4" -->  ["|" ["." "obj" "he"] 1]
def expression_to_list(x):
    y = []
    z = x
    while True:
        for i in range(len(z)):
            if z[i] == '.' or z[i] == '|' or z[i] == '+' or z[i] == '-' or z[i] == '*' or z[i] == '/':
                if len(y) == 0:
                    # []
                    y.append(atom(z[0:i]))
                    y.insert(0, atom(z[i]))
                else:
                    #  y = [. obj]
                    y.append(atom(z[0:i]))
                    # y = [. obj he]
                    y = [atom(z[i]), y]
                z = z[(i+1):]
                break
        else:
            y.append(atom(z))
            break 
    return y              

# 对一个列表调用eval_all必然有一个返回值，返回值有：
# 整数、浮点数、字符串、None、True、False、Python内置函数、类(内置和自定义)、
# 用户自定义变量（包括自定义函数）
def eval_all(x, e):
    while True:
    
        if isa(x, List):
        
            # 空列表
            if len(x) == 0:
                return None
                                
            if len(x) >= 1:                
                    
                # 用于注释
                if x[0] == ';':
                    return None
                                    
                # 打印当前的环境。
                elif x[0] == "show":
                    print("Env {")
                    if len(x) == 2:
                        # ZH内置变量和函数
                        for i in env_g.my.keys():
                            print("\t", i, " : ", env_g.my[i])
                    else:
                        # 自定义变量和函数
                        for i in e.my.keys():
                            print("\t", i, " : ", e.my[i])
                    print("}")
                    return None
                    
                # 列表下标
                elif x[0] == '|':
                    eval_all(x[1], e)
                    eval_all(x[2], e)
                    return eval_all(x[1], e)[eval_all(x[2], e)]
                    
                elif x[0] == 'time':
                
                    start = datetime.datetime.now()
                    eval_all(x[1], e)
                    end = datetime.datetime.now()    
                    print(end - start)
                    return None
                    
                # 定义变量或函数
                # (define (i 12) (a 13) ((fun a) a)))
                elif x[0] == 'define': 
                
                    # "obj.he|1.o"  -->  obj.he|1.o
                    def get_expression(x):
                        for i in x:
                            if i == '.':
                                return None
                                
                    def has_set_op(x):
                        for i in x:
                            if i == '|':
                                return True
                        return False
                
                    for i in x[1:]: 
                    
                        if isa(i, List) == False:
                            print("define的参数必须为列表");
                            
                        if len(i) != 2:
                            print("define每一项参数有且只有两项\n");
                            
                        # 变量定义
                        if isa(i[0], str):
                        
                            # 往外层查找变量，是否定义过？
                            tmp = find_all(i[0], e)
                            if tmp != None:
                                # 为变量赋值,并标记为已经用过.
                                tmp.my[i[0]] = [eval_all(i[1], e), 1]
                            else:
                                # 首次定义变量
                                e.my[i[0]] = [eval_all(i[1], e), 0]
                                
                                '''
                                # 为列表、字典赋值
                                if has_set_op(i[0]):
                                    y = expression_to_list(i[0])
                                    # 为list、对象成员赋值。
                                    #eval_all(y, e) = eval_all(i[1], e)
                                    '''
                        
                        # 函数定义
                        if isa(i[0], List):
                            tmp = find_all(i[0][0], e)
                            if tmp != None:
                                print("函数已定义\n")                                
                            else:
                                e.my[i[0][0]] = [Procedure(i[0][0], i[0][1:], i[1], e), 0] 
                                
                    return None
                
                elif x[0] == 'import':
                    for i in x[1:]:
                        e.my[i] = [__import__(i), 0]
                    return None
                    
                # 异常处理的问题在于，那些语句、函数会触发异常？
                # (try ())
                elif x[0] == 'try':
                    return None
                    
                # 触发一个异常
                elif x[0] == 'raise':
                    raise x[1];
                    
                # 单元测试，确定某个函数的返回值和预期一致。
                elif x[0] == 'test':
                
                    print(x[1], "= ", x[2])
                    a  = eval_all(x[1], e)
                    b  = eval_all(x[2], e)
                    if a != b:
                        print("Fail\t")
                    else:
                        print("OK\t")
                    return None
                
                # 输出多项，返回None
                elif x[0] == 'look':
                    for i in x[1:]:
                        v = eval_all(i, e)
                        if v != None:
                            print(v)
                    return None
                
                # if返回某一项。
                elif x[0] == 'if':
                    (_, test, conseq, alt) = x
                    x = (eval_all(conseq, e) if eval_all(test, e) else eval_all(alt, e))
                
                elif x[0] == 'lambda':
                
                    # (set a (lambda (x y) (+ x y)))
                    # (lambda parms body)
                    if len(x) != 3:
                        print("Error : [lambda] needs 2 args.")
                        return 
                    return Procedure("lambda", x[1], x[2], e)
                    
                elif x[0] == 'while':
                
                    if (len(x) != 3):
                        print("Error : [while] needs 2 args.")
                        
                    while eval_all(x[1], e) == True:
                        has_break = False
                        for i in x[2]:
                            # 检测到break，很可能是跳出循环。
                            if eval_all(i, e) == 'break':
                                has_break = True
                        if has_break == True:
                            break
                    return None
                    
                elif x[0] == 'for':
                
                    c = env(e)
                    
                    # for 有两种型式，一种是C程序中的自增循环；而是Python中的列表循环。               
                    
                    #  (for i l (...)) 列表循环
                    if (len(x) == 4):
                        l = eval_all(x[2], c)
                        for i in l:
                            c.my[x[1]] = [i, 0]
                            eval_all(x[3], c)
                    
                    #  () 自增循环
                    elif (len(x) == 5):
                        eval_all(x[1], e)       # (set (i 1))初始化
                        has_break = False
                        while True:
                            if eval_all(x[2], e) == True:   # 结束条件
                                for i in x[4]:
                                    tmp = eval_all(i, e)
                                    if tmp == 'break':
                                        has_break = True
                                    elif tmp != None:
                                        ##pass
                                        print(tmp)
                                if has_break == True:
                                    break
                            else:
                                break;
                        eval_all(x[3], e)     # (+ i 1) 步长
                    else:
                        print("Error : [for] needs 3 or 4 args.")
                
                    return None
                    
                # (class child father (...) (...))
                elif x[0] == 'class':
                    if x[1] not in e.my.keys():
                        # 类型未定义
                        l = []
                        for i in x[3:]:
                            l.append([i[0], eval_all(i[1], e)])                
                        
                        # type参数：x[1]为子类型，x[2]为父类型，eval把字符串转化为类, 返回的变量指代一个类。
                        # 变量添加到环境变量e里去
                        e.my.update({x[1]: [type(x[1],(type(eval("x[2]()")), ) , dict(l)), 0]})
                    else:
                        print("Error : class [" + x[1] + "] defined again.")
                    
                    return None
                    
                elif x[0] == 'break':
                    return 'break'
                    
                else:        
                    
                    #print(x)
                    
                    if isa(x[0],List):
                        # 第一项是一个列表。则为顺序块，依次eval列表各项，返回最后一项。
                        c = env(e)
                        for exp in x[0:-1]:
                            eval_all(exp, c)
                    
                        #最后一项eval后返回。
                        return eval_all(x[-1], c)                
                    
                    args = []
                    for i in x[1:]:
                        args = args + [eval_all(i, e)]
                    #print(args)               
                    
                    obj = eval_all(x[0], e)
                    
                    #eval单独处理
                    if obj == eval:
                        return obj(*x[1:])

                    if obj == list:
                        return list(args)
                    
                    if obj == tuple:
                        return tuple(args)
                        
                    # 创建一个对象 或 调用Python内置函数
                    elif type(obj) == "type" or type(obj) == types.BuiltinFunctionType:
                        return obj(*args)
                        
                    e0 = find_all(x[0], e)
                    if e0 == env_g:
                        #print(e0.my[x[0]])
                        # Poem内置函数
                        if callable(e0.my[x[0]]):
                            return e0.my[x[0]](*args)
                        else:
                            print("变量%s不能被调用\n", x[0])
                            exit()
                            
                    elif e0 != None:                            
                        #自定义函数。使用之前，将变量对应的列表第二项置为1
                        e0.my[x[0]][1] = 1
                        
                        if callable(e0.my[x[0]][0]):    
                            return e0.my[x[0]][0](*args)
                        else:
                            print(" 变量%s不能被调用\n", x[0])
                            exit()                    
                
                    #没找到，可能是一个中缀表达式。
                    if e0 == None:                  
                        tmp = eval_all(x[0], e)
                        # 这里的调用期望是对象方法
                        if callable(tmp):
                            return tmp(*args)  
                        else:
                            print("未知 -- %s \n", x[0])
                            
                    return 
                        
                    # ['+', ['.', 'obj','m'], 2] 表达式解析
                            # 是一个Python值
                            
        if isa(x, int) or isa(x, float) or isa(x, bool) or isa(x, types.BuiltinFunctionType) or type(x) == type:
            return x
            
        if isa(x, String):
        
            # x在环境变量里
            e0 = find_all(x, e)   
            if e0 != None:                    
                if e0 == env_g:
                    #Poem内置函数或变量
                    return e0.my[x]  
                else:
                    # 用户定义变量或函数
                    e0.my[x][1] = 1
                    return e0.my[x][0]
            
            # (OPEN "TEST.S" "r")
            
            # (+ j|3.n 3)*2-1
            # obj.he|1.o|2:-1  -->  [| [. obj he] 1]
            
            if has_op(x):
                try:
                    y = expression_to_list(x)   
                    return eval_all(y, e)
                except:
                    # 是一个字符串常量      
                    return x
            
            return x
                
        return None
                
def is_blank(line):
    for ch in line:
        if ch != ' ' and ch != '\t' and ch != '\n' and ch != '\r':
            return False
    return True

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(is_blank(" \t   \n"), True)
        self.assertEqual(expression_to_list("obj.m"), ['.','obj', 'm'])
        self.assertEqual(expression_to_list("l|i"), ['|','l', 'i'])
        self.assertEqual(expression_to_list("obj.m+2"), ['+', ['.', 'obj','m'], 2])
        self.assertEqual(expression_to_list("obj.m|2.a|4"), ['|', ['.', ['|', ['.', 'obj','m'], 2], 'a'], 4])

t = MyTest()
t.test()

# 切换到utf-8代码页

os.system("chcp 65001")

if len(sys.argv) == 1:
    # 逐行解释执行用户输入
    repl()
    sys.exit(0)

# 以行为单位读取文件并解释执行。
def eval_as_line(f):
    for line in f:
        if is_blank(line):
            continue
        
        print("...>")
        print(line)
        # 分析列表的意义，并计算。
        val = eval_all(parse(line), e)
        
        # 打印计算结果
        if val is not None: 
            print(val)
          
def eval_file(f):
    program = f.read()
    tmp = get_list(tokenize(program))
    
    val = eval_all(tmp, en)
    # 打印计算结果
    if val is not None: 
        print(val)

if len(sys.argv) == 2:
    f = open(sys.argv[1], "r")
    
    #eval_as_line(f)
    eval_file(f)
        
    f.close()
    
    for i in en.my.keys():
        if isa(en.my[i] ,List) and en.my[i][1] == 0:
            print("Warn : [", i, "] is not used." )
    sys.exit(0)