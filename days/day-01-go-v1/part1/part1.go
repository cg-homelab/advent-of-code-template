package part1

import (
	"strconv"
	"strings"
)

func Process(input string) string {
	sum := 0
	for _, line := range strings.Split(strings.TrimSuffix(input, "\n"), "\n") {
		line = strings.TrimSuffix(line, "\r")
		first, last := -1, -1
		for i := 0; i < len(line); i++ {
			c := line[i]
			if c >= '0' && c <= '9' {
				d := int(c - '0')
				if first < 0 {
					first = d
				}
				last = d
			}
		}
		if first < 0 {
			panic("part1: line without a digit: " + strconv.Quote(line))
		}
		sum += first*10 + last
	}
	return strconv.Itoa(sum)
}
