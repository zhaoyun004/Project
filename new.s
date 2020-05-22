(set f (open "test.ss" "r"))
(print (f.read))

(class point (list (list n "hello!") (list m (lambda x (* 2 x)))))
(set x (point))
(print x.n)
(print (x.m 123))

(set j (list 34 "test" 3 x))
(print j|0)
(print j|1)
(print ([] j 1))

(print j|3.n)
(print (j|3.m 9))