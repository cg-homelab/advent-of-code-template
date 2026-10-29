module Day01.Tests

open System
open System.IO
open Xunit

let private example name =
    File.ReadAllText(Path.Combine(AppContext.BaseDirectory, name))

[<Fact>]
let ``part1 example`` () =
    Assert.Equal("142", Part1.solve (example "example1.txt"))

[<Fact>]
let ``part2 example`` () =
    Assert.Equal("281", Part2.solve (example "example2.txt"))
