-module(fib).
-export([fib/1]).
-export([myfun/0]).
-include_lib("eunit/include/eunit.hrl").
-include_lib("stdlib/include/assert.hrl").

fib(0) -> 0;
fib(1) -> 1;
fib(N) when N > 1 -> fib(N-1) + fib(N-2).

% ? 开头  表示展开一个宏

fib_test_() ->
	[?_assert(fib(0) =:= 0),
	?_assert(fib(1) =:= 1),
	?_assert(fib(2) =:= 1),
	?_assert(fib(3) =:= 2),
	?_assert(fib(4) =:= 3),
	?_assert(fib(5) =:= 5),
	?_assert(fib(6) =:= 8),
	?_assertException(error, function_clause, fib(-1)),
	?_assert(fib(31) =:= 2178309)
	].
	
myfun() ->
	?_assert(12==12).