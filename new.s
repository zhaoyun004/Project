(time
(begin
(define sum 0)
(for (define i 0) (<= i 999) (set i (+ i 1)) (set sum (+ sum i)))
(print sum)
)
)
