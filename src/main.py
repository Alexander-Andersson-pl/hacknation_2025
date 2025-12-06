from rules.static import bank_account

input = "This is my bank account: PL12345678901234567890123456"

static_rules = [bank_account.BankAccount]

str = ""
for word in input.split():
    anonymized = False

    for rule in static_rules:
        token, ok = rule.anonymize(word)
        if ok:
            str += token.label()
            anonymized = True
            break

    if not anonymized:
        str += word
    str += " "

print(str)
