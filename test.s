(define i 1)

(class point (list (list n "hello!!!!!")(list m (lambda x (* 2 x)))))
(define x (point))
(print (. x n))
(procedure? (. x m))
(quote here are bugs)
(. x m)

(define fun (begin (define i 12) 34))

(if (< i 19) (print (+ i 1))
    )
    
(while (< i 23) (begin (print i) (set i (+ i 1))(if (eq? i 12) break)))

(define sum 0)
(for (set i 0) (< i 100) (set i (+ i 1)) (+ sum i))
(print sum)

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
