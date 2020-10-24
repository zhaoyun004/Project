(
(define (ab (' "first.s" "second.s" "third.s" "new.s" "newton.s" "scheme.s")))

 (; 处理字符串中的空格？)
(for i ab (os.system (+ "python poem.py" i)))

)