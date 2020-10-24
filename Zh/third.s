(
(define (m "hello"))
(print m|0)

(define (i 12))
(define (a 12) (b 23) (c 34))

(define ((circle_area r) (* pi (* r r))))
(print (circle_area 3))

(if (< i 19) (print (+ i 1)) (print "aaa"))

(while (< i 23) (
    (print i) 
    (define (i (+ i 1)))
    (if (eq? i 19) break ())
))

(define ((mysum x r)
    (if (eq? x 0)
        r
        (mysum (- x 1) (+ x r))
    )
	)
)

(print (int "12123"))
(test (mysum 100 0) 5050)


(tuple (list 12 34))
(list (tuple 12 34))

(define (s 0))

(; wrong here? because for statment wrong )
(for (define (i 0)) (< i 101) (define (i (+ i 1))) 
    (define (s (+ s i)))
) s

(quote
(import scheme.s)
(import newton.s)
(import "http://test.org/test.s" "test")
)
)