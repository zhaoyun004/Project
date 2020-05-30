#!/usr/bin/env escript
%%! -smp enable -sname mmcshadow -mnesia debug verbose[/color]

main([String]) ->
  io:format("args ~p~n",[String]);
  
main([Str1,Str2]) ->
  io:format("two args ~p ~p~n",[Str1,Str2]);

main([Str1,Str2,Str3]) ->
  io:format("three args ~p ~p ~p ~p~n",[Str1,Str2,Str3,node()]);

main(_) ->
	Pi = math:pi(),
	io:format("Pi is ~5.2f\n", [Pi]),
	io:format("zero args~n"),
	io:format("Pi is ~10#\n", [len([1,2,3,4,7])]).

len(L) -> len(L,0).   %% 这其实只是给 len/2 的第二个参数设置了一个默认值 0.
len([], Acc) -> Acc;  %% 所有的元素都读完了
len([_|T], Acc) -> len(T,Acc+1).  %% 读一个元素，Acc 增1，然后计算剩下的 List 的长度。\

%% 注意，函数语句结尾“. ; ,”。  