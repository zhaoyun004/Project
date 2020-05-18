(set i 12)
(tuple 2 3)
(print (dict (list (list "3" 4) (list "aa" "bbb"))))

(goto "test")

(if (< i 19) (print (+ i 1)))

(while (< i 23) (begin (print i) (set i (+ i 1))(if (eq? i 20) break)))

(for (set i 23) (< i 45) (set i (+ i 2)) (begin (print i) (if (eq? i 43) break)))

(set sum 0)
(for-each (lambda (x) (set sum (+ sum x))) (list 3 4 5 6 7))
(print sum)

(label "test")

(set abc 123)


(define (fun (x y) (m n)) (begin (set i "testykasd") (return (12 34)) (env)))
(set (a b) (fun x y))
(print i)