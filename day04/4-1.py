start = 246540
end = 787419

rule1 = set()
rule2 = set()

for code in range(start, end):
    for i in ('00', '11', '22', '33', '44', '55', '66', '77', '88', '99'):
        if i in str(code):
            rule1.add(code)

for code in range(start, end):
    cmpr = str(code)[0]
    bad = False
    for digit in str(code)[1:]:
        if digit < cmpr:
            bad = True
        cmpr = digit
    if not bad:
        rule2.add(code)

answer = len(rule2&rule1)
print(answer)