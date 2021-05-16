
def transition(state, letter):
    next_state, output = "", ""
    if letter == "#":
        if state in ["ก", "ต", "ส", "พ", "ห", "ด", "ฟ", "ล", "ย", "น", "ฉ"]:
            return "", state
    if state == "":
        if letter in ["ก",  "ต", "ส", "พ", "ห", "ด", "ฟ", "ล", "จ1", "ย",  "น", "ฉ1"]:
            next_state, output = letter, ""
        elif letter in ["บ", "ร", "ว", "ม",  "อ"]:
            next_state, output = "", letter
        else:
            next_state, output = "", ""
    elif state == "ก":
        if letter in "123":
            next_state, output = "", "ขคฆ"[int(letter)-1]
        else:
            ns, op = transition("", letter)
            next_state, output = ns, "ก" + op
    elif state == "ต":
        if letter in "12345":
            next_state, output = "", "ถฐฒฑฏ"[int(letter)-1]
        elif letter == "ห":
            next_state, output = "ท", ""
        else:
            ns, op = transition("", letter)
            next_state, output = ns, "ต" + op
    elif state == "ท":
        if letter == "1":
            next_state, output = "", "ธ"
        else:
            next_state, output = "", "ท"
    elif state == "ส":
        if letter in "12":
            next_state, output = "", "ศษ"[int(letter)-1]
        elif letter == "ซ2":
            next_state, output = "", "ซ"
        else:
            ns, op = transition("", letter)
            next_state, output = ns, "ส" + op
    elif state == "พ":
        if letter in "123":
            next_state, output = "", "ปผภ"[int(letter)-1]
        else:
            ns, op = transition("", letter)
            next_state, output = ns, "พ" + op
    elif state == "ห":
        if letter == "1":
            next_state, output = "", "ฮ"
        else:
            ns, op = transition("", letter)
            next_state, output = ns, "ห" + op
    elif state == "ด":
        if letter == "1":
            next_state, output = "", "ฎ"
        else:
            ns, op = transition("", letter)
            next_state, output = ns, "ด" + op
    elif state == "ฟ":
        if letter == "1":
            next_state, output = "", "ฝ"
        else:
            ns, op = transition("", letter)
            next_state, output = ns, "ฟ" + op
    elif state == "ล":
        if letter == "1":
            next_state, output = "", "ฬ"
        else:
            ns, op = transition("", letter)
            next_state, output = ns, "ล" + op
    elif state == "จ1":
        if letter == "จ2":
            next_state, output = "", "จ"
        else:
            next_state, output = "", ""
    elif state == "ย":
        if letter == "1":
            next_state, output = "", "ญ"
        else:
            ns, op = transition("", letter)
            next_state, output = ns, "ย" + op
    elif state == "น":
        if letter == "1":
            next_state, output = "", "ณ"
        elif letter == "ง2":
            next_state, output = "", "ง"
        else:
            ns, op = transition("", letter)
            next_state, output = ns, "น" + op
    elif state == "ฉ1":
        if letter == "ห":
            next_state, output = "ฉ", ""
        else:
            next_state, output = "", ""
    elif state == "ฉ":
        if letter in "12":
            next_state, output = "", "ชฌ"[int(letter)-1]
        else:
            ns, op = transition("", letter)
            next_state, output = ns, "ฉ" + op
    return (next_state, output)


def sequence_to_text(sequence):
    text = ""
    state = ""
    seq_with_end = sequence + ["#"]
    for letter in seq_with_end:
        next_state, output = transition(state, letter)
        state = next_state
        text += output
    return text
