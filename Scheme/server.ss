#lang Racket

(define the-listener (tcp-listen 9876))
(define-values (in out) (tcp-accept the-listener))
(displayln (read in))
(write  "from server" out)
(tcp-close the-listener)