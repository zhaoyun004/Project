#!/usr/bin/env escript

main(_) ->
	% ok 是一个atom类型，在ErLang里，atom只能用于比较是否相同， 内部可能使用整数来代表某个atom
	{ok, Listen} = gen_tcp:listen(2345, [binary, {packet, 4}, {reuseaddr, true}, {active, true}]),
	% {ok, Listen} = gen_tcp:listen(2345, [binary, {packet, 4}, {ip,{127,0,0,1}}, {active, true}]).
	{ok, Socket} = gen_tcp:accept(Listen),
	{ok,{IP_Address,Port}} = inet:peername(Socket),
	io:format("[~p][~p] ~n", [IP_Address, Port]),
	gen_tcp:close(Socket).