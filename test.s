(set i 12)

(if (< i 19) (print (+ i 1)))
    
(while (< i 23) (begin 
    (print i) 
    (set i (+ i 1))
    (if (eq? i 19) break)
    )
)

(set s 0)
(for (set i 0) (< i 101) (set i (+ i 1)) 
    (set s (+ s i))
)
(print s)
   
(define (sum x r)
    (if (eq? x 0)
        (print r)
        (sum (- x 1) (+ x r))
     )
)
(sum 500 0)

(set m 12)
(set fun (lambda x (* x x)))
(print (fun m))

(quote
(import scheme.s)
(import "http://test.org/test.s" "test")
)