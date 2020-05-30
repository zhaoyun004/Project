-module(useless).
-export([add/2, add/3]). %% export 是导出语法，指定导出 add/2, add/3 函数。没导出的函数在 Module 外是无法访问的。

add(A, B) ->
  A + B.
add(A, B, C) ->
  A + B + C.