(class point (list (list n "hello!")(list m (lambda x (* 2 x)))))
(set x (point))
(print (. x n))
(procedure? (. x m))
(print ((. x m) 5))


(set f (open test.ss r))
(print ((. f read)))