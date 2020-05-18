(set i 12)

(if (< i 19) (print (+ i 1))
    )
    
(while (< i 23) (begin (print i) (set i (+ i 1))(if (eq? i 19) break)))

(set s 0)
(for (set i 0) (< i 101) (set i (+ i 1)) (set s (+ s i)))
(print s)

(set t 0)
(define (sum x r)
      (if (eq? x 0)
          r
          (sum (- x 1) (+ x r))
       )
)
(sum 150 t)
(print "....")
(print t)
(print "....")