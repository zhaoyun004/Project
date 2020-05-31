-module(tut14).

-export([start/0, say_something/2]).

-export([add/2, add/3]). 
%% export 是导出语法，指定导出 add/2, add/3 函数。
%% 没导出的函数在 Module 外是无法访问的。

add(A, B) ->
  A + B.
add(A, B, C) ->
  A + B + C.

say_something(What, 0) ->
    done;
say_something(What, Times) ->
    io:format("~p~n", [What]),
    say_something(What, Times - 1).

start() ->
    spawn(tut14, say_something, [hello, 3]),
    spawn(tut14, say_something, [goodbye, 3]).