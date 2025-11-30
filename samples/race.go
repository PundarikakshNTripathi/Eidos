// samples/race.go
// Goal: Test analyze_assembly_essence (Go) or general Go support

package main

import "fmt"

func main() {
    c := make(chan int)
    go func() { c <- 1 }()
    fmt.Println(<-c)
}
