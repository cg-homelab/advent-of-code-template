module Day01.Part2

open System

let private words =
    [| "one"; "two"; "three"; "four"; "five"; "six"; "seven"; "eight"; "nine" |]

// Digit (1..9) starting at index i, either as a word or an ASCII digit; -1 if none.
let private digitAt (line: string) (i: int) : int =
    let c = line.[i]
    let mutable result = -1
    for w in 0 .. words.Length - 1 do
        if result < 0 && String.CompareOrdinal(line, i, words.[w], 0, words.[w].Length) = 0 then
            result <- w + 1
    if result < 0 && c >= '0' && c <= '9' then int (c - '0') else result

let private lineValue (line: string) : int =
    let line = line.TrimEnd('\r')
    let mutable first = -1
    let mutable last = -1
    for i in 0 .. line.Length - 1 do
        let d = digitAt line i
        if d >= 0 then
            if first < 0 then first <- d
            last <- d
    if first < 0 then failwith ("no digit found in line: " + line)
    first * 10 + last

let solve (input: string) : string =
    input.TrimEnd('\n').Split('\n')
    |> Array.sumBy lineValue
    |> string
