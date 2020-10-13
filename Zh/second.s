(; "尾调用优化")

(set (f (open "test.s" "r")))
(set (s (f.read))) s

(define (testa x) x ) 

(testa 12)

(class point object 
    (set (n 12) (fun (lambda x (* 2 x))))
)

(set (a (point))) a

(quote "类未使用没有警告")

(class envi object 
    (set (my (dict ('))) (father nil)(setfa (lambda x (set (father x)))))
)

(env)  (set (env_g (envi))) env_g

(set (d (dict (' (' "+" +) 
    (' "-" -)
    (' "*" *)
    (' "/" /)
	(' "test" "ttt")
    )))
) 

(env_g.my.update d) env_g.my
(set (l (list (d.keys)))) l ()
