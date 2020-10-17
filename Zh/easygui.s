(define (f (open "test.gui" "r")))
(define (l (f.readlines)))

(for (define (i 0)) (< i (len l)) (define (i (+ i 1))) ((l|i) "----"))

tkinter
(define (top (tkinter::Tk)))
top
(define (label (tkinter::Label top "data")))
label
label.pack
(tkinter::mainloop)

()