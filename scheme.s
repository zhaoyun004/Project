(set i 12)
(tuple 2 3)
(print (dict (list (list "3" 4) (list "aa" "bbb"))))

(if (< i 19) (print (+ i 1)))

(while (< i 23) (begin (print i) (set i (+ i 1))(if (eq? i 20) break)))

(for (set i 23) (< i 45) (set i (+ i 2)) (begin (print i) (if (eq? i 43) break)))

(set sum 0)
(for-each (lambda (x) (set sum (+ sum x))) (list 3 4 5 6 7))
(print sum)

(set abc 123)


(define (fun) (begin (set i "testykasd") 34 (env)))
(fun)
(print i)