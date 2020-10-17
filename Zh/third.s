(define (i 12))
(define (a 12) (b 23) (c 34))

(define (circle_area (lambda (r) (* pi (* r r)))))
(circle_area 3)

(if (< i 19) (+ i 1) "aaa")

(while (< i 23) (
    (print i) 
    (define (i (+ i 1)))
    (if (eq? i 19) break ())
))

(define (s 0))


(; wrong here? because for statment wrong )

(for (define (i 0)) (< i 101) (define (i (+ i 1))) 
    (define (s (+ s i)))
) s

(define (sum x r)
    (if (eq? x 0)
        r
        (sum (- x 1) (+ x r))
     )
)

(print (int "12123"))
(test (sum 100 0) 5050)

(define (m "hello"))
(print m|3)

(quote
(import scheme.s)
(import newton.s)
(import "http://test.org/test.s" "test")
)