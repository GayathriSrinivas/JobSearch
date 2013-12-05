#! /usr/bin/python

letters = map(chr, range(97, 97 + 26))
maxlen = 3

generated = letters[:]
for i in range(2, maxlen + 1):
    n = len(generated)
    for j in range(n):
        for letter in letters:
            generated.append("%s%s" % (generated[j], letter))

generated = sorted(list(set(generated)))
print generated
