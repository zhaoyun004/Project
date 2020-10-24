(; "牛顿法求平方根")

(define (mysqrt x) (begin
    (print x)
     
	 (; "函数A内定义的函数只在函数A内可见")
	 
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
    
    (test (average 7 6) 6.5)
    (test (improve 1) 5)
    (test (good-enough? 1.41) False)
    
	(; "猜1.4是平方根结果")
    (sqrt-iter 1.4)
    )
)
(mysqrt 9)
(mysqrt 8)
(mysqrt 16)

(show)
 (; "这里应该报错")
(averageasf 7 9)
12
   