(; "尾调用优化")

(define (f (open "test.s" "r")))
(define (s (f.read))) s

(define (testa x) x ) 

(testa 12)

(class point object 
    (define (n 12) (fun (lambda x (* 2 x))))
)

(define (a (point))) a

(quote "类未使用没有警告")

(class envi object 
    (define (my (dict ('))) (father nil)(define fa (lambda x (define (father x)))))
)

(env)  (define (env_g (envi))) env_g

(define (d (dict (' (' "+" +) 
    (' "-" -)
    (' "*" *)
    (' "/" /)
	(' "test" "ttt")
    )))
) 

(env_g.my.update d) env_g.my
(define (l (list (d.keys)))) l ()
