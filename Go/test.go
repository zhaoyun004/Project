package main

import (
    "fmt"
    "time"
    "github.com/ccding/go-stun/stun"
)

func test_print(a int){
    fmt.Println(a)
}

func main(){
    for i:= 0;i < 100; i ++ {
        go test_print(i)
    }
    time.Sleep(time.Second)
    
    nat, host, err := stun.NewClient().Discover()
    fmt.Println(nat)
    fmt.Println(host)
    fmt.Println(err)
}

/*在实现高并发的时候只需要在调用的函数前面加上go，就表示开启了并发。

如果在for循环的外面不加上time.Sleep(time.Second)，就会发现会少打印了，

这是因为当主程序运行完之后，并不会等待线程，所以程序直接终止*/