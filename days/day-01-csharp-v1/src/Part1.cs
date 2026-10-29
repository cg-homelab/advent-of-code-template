namespace Day01;

public static class Part1
{
    public static string Process(string input)
    {
        var sum = 0;
        foreach (var raw in input.TrimEnd('\n').Split('\n'))
        {
            var line = raw.TrimEnd('\r');
            var first = -1;
            var last = -1;
            foreach (var c in line)
            {
                if (c is >= '0' and <= '9')
                {
                    if (first < 0)
                    {
                        first = c - '0';
                    }
                    last = c - '0';
                }
            }
            if (first < 0)
            {
                throw new InvalidOperationException($"No digit found in line: '{line}'");
            }
            sum += first * 10 + last;
        }
        return sum.ToString();
    }
}
