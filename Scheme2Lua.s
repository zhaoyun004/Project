(quote "该文件用于将Scheme文件转化为Lua字节码")
(set (f (open "test.s" "r")))
(set (s (f.read)))
(print s)

(quote "类未使用没有警告")
(class envi (list
    (list my (dict (list)))
    (list father nil)
    (list setfa (lambda x (set (father x))))
    )
)

(set (env_g (envi)))

(set (d (dict (list (list "+" +) (list "-" -)))))

(env_g.my.update d)
    
(print env_g.my)

(define (eval_list l e)
    ()
)