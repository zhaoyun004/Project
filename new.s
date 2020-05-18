(quote ...)

(class point (list (list n "hello!!!!!")(list m (lambda x (* 2 x)))))
(set x (point))
(print (. x n))
(procedure? (. x m))
(quote here are bugs)
(. x m)

(set f (open test.ss r))
((. f read))


(print (call/cc (lambda k (* 5 (k 8) 45))))

(print (call/cc (lambda (k) (begin 5 4 (k (list 7 4 5)) 3 6))))

(print
(call/cc (lambda (k) (begin (set i 0)(while (< i 10)(begin (if (= i 6)(k 123)(begin (print i) (set i (+ i 1)))))))))
)