#lang Racket

;ChezSchme打开汇编输出
(#%$assembly-output #t)

(integer? 12)
(real? 12.4)
(string? "abc")
(symbol? 'a)
(atom? 12)

(list? (cons 3 4))

;quote或者'用于注释一对()之间的内容。
(quote (+ 1 2))

;list构造一个列表, list和+都是系统内置函数(procudre)
(list + 1 2)
(list (lambda x (+ x 1)) 3 4 list)

;(procedure? quote)会导致语法错误，说明quote不是内置函数，也许算是“关键字”或者“保留字”
(procedure? list)
(procedure? values)
(procedure? +)

(define-values (x y) (values 1 2))

(define xy 123)
(define-values (get-x put-x!)
       (values
       (lambda () xy)
       (lambda (v) (set! xy v))))


;以begin开始的语句块,其中的语句将顺序执行,最后一项是函数的返回值 
; lambda函数体也一样。
(define (fun x) (begin (display "abc") '(12 3 54) '("abcd")))
;x的值为`("abcd")
(define y (fun 6))


(define newdisplay (lambda (x) (begin (display x)(newline))))
(define tt (lambda args (for-each newdisplay args)))
(tt 'abc 'efg 'tomson)


(eval '(+ 1 2))
(apply + (list 1 3 5 6))


;字典 -- 一种常见的数据结构， Python,JavaScript中都有该结构
(define z (list (cons "Dict" "字典") (cons "test" "测试")))


;交换变量
(define m 10)
(define n 12)
(define t)
(set! t m)
(set! m n)
(set! n t)


(define a (list 1 2 3 4))     ; a is '(1 2 3 4)

(define (list-set! list k val)
    (if (zero? k)
        (set-car! list val)
        (list-set! (cdr list) (- k 1) val)))

(list-set! a 2 100)           ; a is '(1 2 100 4)

(set-car! (list-tail a 2) 716)


(define new-table (make-vector 3 (make-vector 3 #f)))
(vector-set! (vector-ref new-table 0) 0 42) ; we modify a single position ...


;写文件
(define out (open-output-file "some-file-1"))
(display "hello world" out)
;(close-ouput-port out)


;call/cc函数，接受一个函数作为参数，并且，作为参数的函数也只能有一个参数。
(define fun (lambda (k) 5 4 (k (list 7 4 5)) 3 6))
(fun display)

;普通的函数调用，返回函数定义中的最后一项列表的计算结果, 而call/cc调用，则可以让函数在计算任意一项列表后返回其结果，同时中止该函数的计算。
;
(call/cc fun)

(call/cc (lambda (return)
        (for-each (lambda (x) (if (< x 0) (return x)))
                '(99 88 77 66 55))
        #t))
        
(call/cc (lambda (return)
         (for-each (lambda (x) (if (< x 0) (return x)))
                '(11 22 33 44 -55 66 77))
        #t))