const std = @import("std");

pub fn process(gpa: std.mem.Allocator, input: []const u8) std.mem.Allocator.Error![]u8 {
    var total: u64 = 0;
    var lines = std.mem.splitScalar(u8, std.mem.trimEnd(u8, input, "\n"), '\n');
    while (lines.next()) |raw| {
        const line = std.mem.trimEnd(u8, raw, "\r");
        var first: ?u8 = null;
        var last: u8 = 0;
        for (line) |c| {
            if (std.ascii.isDigit(c)) {
                const d = c - '0';
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
    const answer = try process(std.testing.allocator, @embedFile("example1"));
    defer std.testing.allocator.free(answer);
    try std.testing.expectEqualStrings("142", answer);
}
