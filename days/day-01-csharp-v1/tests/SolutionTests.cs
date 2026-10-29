namespace Day01.Tests;

public class SolutionTests
{
    private static string Example(string name) =>
        File.ReadAllText(Path.Combine(AppContext.BaseDirectory, name));

    [Fact]
    public void Part1Example() =>
        Assert.Equal("142", Part1.Process(Example("example1.txt")));

    [Fact]
    public void Part2Example() =>
        Assert.Equal("281", Part2.Process(Example("example2.txt")));
}
