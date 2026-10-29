namespace Day01;

public static class Part2
{
    private static readonly string[] Words =
    [
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    ];

    public static string Process(string input)
    {
        var sum = 0;
        foreach (var raw in input.TrimEnd('\n').Split('\n'))
        {
            var line = raw.TrimEnd('\r');
            var first = -1;
            var last = -1;
            for (var i = 0; i < line.Length; i++)
            {
                var d = DigitAt(line, i);
                if (d < 0)
                {
                    continue;
                }
                if (first < 0)
                {
                    first = d;
                }
                last = d;
            }
            if (first < 0)
            {
                throw new InvalidOperationException($"No digit found in line: '{line}'");
            }
            sum += first * 10 + last;
        }
        return sum.ToString();
    }

    private static int DigitAt(string line, int i)
    {
        for (var w = 0; w < Words.Length; w++)
        {
            if (line.AsSpan(i).StartsWith(Words[w], StringComparison.Ordinal))
            {
                return w + 1;
            }
        }
        var c = line[i];
        return c is >= '0' and <= '9' ? c - '0' : -1;
    }
}
