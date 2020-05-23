(set (f (open "test.ss" "r")))
(print (f.read))

(class point (list 
    (list n 12) 
    (list m (lambda x (* 2 x))))
)

(set (x (point)))
(print x.n)
(print (x.m 123))

(set (j (list 34 "test" 3 x)))
(print j|0)
(print j|1)
(print (| j 1))
(set (j|0 12))

(print j|3.n+3*2-1)
(print (j|3.m 9))