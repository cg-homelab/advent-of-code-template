const std = @import("std");

const words = [_][]const u8{ "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" };

fn digitAt(line: []const u8, i: usize) ?u8 {
    if (std.ascii.isDigit(line[i])) return line[i] - '0';
    for (words, 1..) |word, value| {
        if (std.mem.startsWith(u8, line[i..], word)) return @intCast(value);
    }
    return null;
}

pub fn process(gpa: std.mem.Allocator, input: []const u8) std.mem.Allocator.Error![]u8 {
    var total: u64 = 0;
    var lines = std.mem.splitScalar(u8, std.mem.trimEnd(u8, input, "\n"), '\n');
    while (lines.next()) |raw| {
        const line = std.mem.trimEnd(u8, raw, "\r");
        var first: ?u8 = null;
        var last: u8 = 0;
        for (0..line.len) |i| {
            if (digitAt(line, i)) |d| {
                if (first == null) first = d;
                last = d;
            }
        }
        const f = first orelse @panic("line without a digit");
        total += @as(u64, f) * 10 + last;
    }
    return gpa.print("{d}", .{total});
}

test "example" {
    const answer = try process(std.testing.allocator, @embedFile("example2"));
    defer std.testing.allocator.free(answer);
    try std.testing.expectEqualStrings("281", answer);
}
