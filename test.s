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


(quote "牛顿迭代迭代法求平方根")

(define (sqrt-iter guess x)
    (if (good-enough? guess x)
         guess
        (sqrt-iter (improve guess x) x) 
    )
)

(define (improve guess x)
    (average guess (/ x guess))
)

(define (average x y)
    (/ (+ x y) 2)
)

(define (good-enough? guess x) 
    (< (abs (- (* guess guess) x)) 0.0001)
)

(print (average 7 6))
(print (improve 1 5))
(print (good-enough? 1.41 3))

(print (sqrt-iter 1 4))


(quote
(import scheme.s)
(import "http://test.org/test.s" "test")
)