(set f (open "test.ss "r))
(print (f.read))

(class point (list (list n "hello!") (list m (lambda x (* 2 x)))))
(set x (point))
(print x.n)
(print (x.m 123))