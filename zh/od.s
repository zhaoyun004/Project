(quote "该程序的作用是以二进制模式打印文件")
(set (f (open "luac.out" "rb")))
(set (s (f.read)))
(print s)

(quote
' '.join(format(ord(x), 'x') for x in st)
)

(set (t ";"))

(print (t.join (' "hello" "world")))

(define (myexpect x y) (if (!= (x) y)
    (print "PASS")
    (print "Not Expect!")
))

(myexpect (' + 3 4) 7)