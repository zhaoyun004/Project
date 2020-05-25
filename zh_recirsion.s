(; "尾调用优化")

(set (f (open "test.s" "r")))
(set (s (f.read)))
(print s)

(quote "类未使用没有警告")
(class envi ('
    (' my (dict (')))
    (' father nil)
    (' setfa (lambda x (set (father x))))
    )
)

(set (env_g (envi)))

(set (d (dict (' (' "+" +) 
    (' "-" -)
    (' "*" *)
    (' "/" /)
    )))
)

(env_g.my.update d)

(set (l (' (d.keys))))

(define (format d)
    (for-each (lambda x (print x ":" (~ d x))) l|0)
)

(format d)

()
(define (eval_list l e)
    ()
)