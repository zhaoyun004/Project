(time
(begin

(quote ...)
(define abc 123)
(define (efg  x) (x))

   (define sum 0)
   (for-each (lambda (x) (set sum (+ sum x))) (list 3 4 5 6 7))
   (print sum)
)
)