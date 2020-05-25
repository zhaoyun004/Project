(; "牛顿法求平方根")

(define (mysqrt x) (begin

    (define (sqrt-iter guess)
        (if (good-enough? guess)
            guess
            (sqrt-iter (improve guess x) x) 
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
    
    (print (sqrt-iter 1.4 x))
    
    )
)
(mysqrt 9)