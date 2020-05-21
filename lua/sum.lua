--Lua实现了尾调用优化
function sum(num, s)
    if (num == 0) then
        return s;
    else 
        return sum(num - 1, s + num);
    end
end

print(sum(10099, 0))