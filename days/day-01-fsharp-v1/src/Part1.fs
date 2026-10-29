module Day01.Part1

// Named `solve` rather than `process`: `process` is reserved for future use
// in F# and triggers warning FS0046.
let private isDigit (c: char) = c >= '0' && c <= '9'

let private lineValue (line: string) : int =
    let line = line.TrimEnd('\r')
    let first = line |> Seq.tryFind isDigit
    let last = line |> Seq.tryFindBack isDigit
    match first, last with
    | Some f, Some l -> int (f - '0') * 10 + int (l - '0')
    | _ -> failwith ("no digit found in line: " + line)

let solve (input: string) : string =
    input.TrimEnd('\n').Split('\n')
    |> Array.sumBy lineValue
    |> string
