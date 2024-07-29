def getNum(start, end, flag):
    flag = "".join(flag)
    return flag[start:end]

with open("flag.enc","r") as f:
    enc = f.read()

flag_enc = "".join([str(ord(i) - 100) for i in enc])

flag_dec = []
start = 0
end = 3
flag_enc = list(flag_enc)
while flag_enc:
    enc = getNum(start, end, flag_enc)

    if int(enc) > 0xff:
        end = 2
        continue

    if int(enc) < 126:
        flag_dec.append(int(enc))
        flag_enc = list(flag_enc)
        del flag_enc[start: end]
        end = 3
    else:
        del flag_enc[start: end]
    
print("".join([chr(i) for i in flag_dec]))