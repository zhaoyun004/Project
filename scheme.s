(begin

(define i 12)

(if (< i 19) (print (+ i 1)))

(while (< i 23) (begin (print i) (set i (+ i 1))(if (eq? i 12) break)))

(for (set i 23) (< i 45) (set i (+ i 2)) (begin (print i) (if (eq? i 43) break)))

(class point (list (list n "hello!!!!!")(list m (lambda x (* 2 x)))))
(define x (point))
(print (. x n))
(procedure? (. x m))
(quote here are bugs)
(. x m)

(print (dict (list (list "3" 4) (list "aa" "bbb"))))
 
)

