(define (j (list 34 "test" 3 4)))
(print j|0)
(print j|1)
(print (| j 1))

(tuple 2 3)

(define (d (dict (list 
    (list "3" 4) 
    (list "aa" "bbb")) ) 
))

(print (d.keys))

(define (t (dict (list (list "name" d)))))
(print t)
(env)

(print (: t "name"))

(define (i 1))
(if (< i 19) (print (+ i 1)) ())

(while (< i 23) ( 
    (print i) 
    (define (i (+ i 1)))
    (if (eq? i 20) break ()))
 )

(for (define (i 23)) (< i 45) (define (i (+ i 2))) ( 
    (print i) 
    (if (eq? i 43) break ()))
)

(define (sum 0))
(each (lambda (x) (define (sum (+ sum x)))) (list 3 4 5 6 7 22))
(print sum)

(define (abc 123))

(define (s 12))
(define (fun x y) (begin 
        (define (s (+ x y))) (print s) (env)
        (define (inside-fun x ) (* x x))
        (print (inside-fun 7))
    )
)
(fun 33 44)
(print s)
()