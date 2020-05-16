(begin (define i 1)

(if (< i 19) (print (+ i 1))
    )
    
(while (< i 23) (begin (print i) (set i (+ i 1))(if (eq? i 12) break)))

(for (set i 23) (< i 45) (set i (+ i 2)) (begin (print i) (if (eq? i 41) break)))

(print (call/cc (lambda k (* 5 (k 8) 45))))

(print (call/cc (lambda (k) (begin 5 4 (k (list 7 4 5)) 3 6))))

(print
(call/cc (lambda (k) (begin (define i 0)(while (< i 10)(begin (if (= i 6)(k 123)(begin (print i) (set i (+ i 1)))))))))
)

(begin 
  (define (sum x r)
      (if (eq? x 0)
          r
          (sum (- x 1) (+ x r))
       )
    )
   (sum 150 0)
)
(sum 100 0)
)
