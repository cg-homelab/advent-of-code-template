package part2

import (
	"strconv"
	"strings"
)

var words = [...]string{"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}

func Process(input string) string {
	sum := 0
	for _, line := range strings.Split(strings.TrimSuffix(input, "\n"), "\n") {
		line = strings.TrimSuffix(line, "\r")
		first, last := -1, -1
		for i := 0; i < len(line); i++ {
			d := -1
			for n, w := range words {
				if strings.HasPrefix(line[i:], w) {
					d = n + 1
					break
				}
			}
			if d < 0 && line[i] >= '0' && line[i] <= '9' {
				d = int(line[i] - '0')
			}
			if d < 0 {
				continue
			}
			if first < 0 {
				first = d
			}
			last = d
		}
		if first < 0 {
			panic("part2: line without a digit: " + strconv.Quote(line))
		}
		sum += first*10 + last
	}
	return strconv.Itoa(sum)
}
