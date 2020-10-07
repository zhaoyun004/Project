(; "牛顿法求平方根")

(define (mysqrt x) (begin
    (print x)
     
    (define (sqrt-iter guess)
        (if (good-enough? guess)
            guess
            (sqrt-iter (improve guess)) 
        )
    )
    
    (define (improve guess)
        (average guess (/ x guess))
    )
    
    (define (average a b)
        (/ (+ a b) 2)
    )
    
    (define (good-enough? guess) 
        (< (abs (- (* guess guess) x)) 0.0001)
    )
    
    (print (average 7 6))
    (print (improve 1))
    (print (good-enough? 1.41))
    
    (sqrt-iter 1.4)
    )
)
(mysqrt 9)
()

   