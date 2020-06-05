(quote "读取一个GUI排版文件，解释执行图形程序。")
(set (f (open "test.gui" "r")))
(set (l (f.readlines)))

(for (set (i 0)) (< i (len l)) (set (i (+ i 1))) ((l|i) "----"))

()