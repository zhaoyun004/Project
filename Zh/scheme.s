(set (j (list 34 "test" 3 4)))
(print j|0)
(print j|1)
(print (| j 1))

(tuple 2 3)

(set (d (dict (list 
    (list "3" 4) 
    (list "aa" "bbb")) ) 
))

(print (d.keys))

(set (t (dict (list (list "name" d)))))
(print t)
(env)

(print (: t "name"))

(set (i 1))
(if (< i 19) (print (+ i 1)) ())

(while (< i 23) ( 
    (print i) 
    (set (i (+ i 1)))
    (if (eq? i 20) break ()))
 )

(for (set (i 23)) (< i 45) (set (i (+ i 2))) ( 
    (print i) 
    (if (eq? i 43) break ()))
)

(set (sum 0))
(each (lambda (x) (set (sum (+ sum x)))) (list 3 4 5 6 7 22))
(print sum)

(set (abc 123))

(set (s 12))
(define (fun x y) (begin 
        (set (s (+ x y))) (print s) (env)
        (define (inside-fun x ) (* x x))
        (print (inside-fun 7))
    )
)
(fun 33 44)
(print s)
()