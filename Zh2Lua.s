(quote "该文件用于将Scheme文件转化为Lua字节码")
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

(set (l (list (d.keys))))

(define (format d)
    (for-each (lambda x (print x ":" (~ d x))) l|0)
)

(format d)

(define (eval_list l e)
    ()
)

