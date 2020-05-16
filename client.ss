#lang racket

(define-values (in out) (tcp-connect "localhost" 9876))
(write "Hello" out)
(flush-output out)
;(displayln (read in))
(close-input-port in)
(close-output-port out)
(display "end")