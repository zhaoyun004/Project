(set (i 12))
(set (a 12) (b 23) (c 34))

(set (circle_area (lambda (r) (* pi (* r r)))))
(circle_area 3)

(if (< i 19) (+ i 1) "aaa")
    
(while (< i 23) (
    (print i) 
    (set (i (+ i 1)))
    (if (eq? i 19) break ())
))

(set (s 0))
(for (set (i 0)) (< i 101) (set (i (+ i 1))) 
    (set (s (+ s i)))
) s

(define (sum x r)
    (if (eq? x 0)
        r
        (sum (- x 1) (+ x r))
     )
)

(print (int "12123"))
(test (sum 100 0) 50560)

(set (m "hello"))
(print m|3)

(quote
(import scheme.s)
(import newton.s)
(import "http://test.org/test.s" "test")
)

()