#lang Racket
(require 2htdp/image)
(require 2htdp/planetcute)

; stack : non-empty-list-of-images -> image
; stacks 'imgs' on each other, separated by 40 pixels
(define (stack imgs)
  (cond
    [(empty? (rest imgs)) (first imgs)]
    [else (overlay/xy (first imgs)
                      0 40
                      (stack (rest imgs)))]))

(beside/align
   "bottom"
   (stack (list wall-block-tall stone-block))
   (stack (list character-cat-girl
                stone-block stone-block
                stone-block stone-block))
   water-block
   (stack (list grass-block dirt-block))
   (stack (list grass-block dirt-block dirt-block)))