from rules.static import bank_account, name, credit_card, email, pesel_rule

input = "Nazywam się Jan Kowalski, mój PESEL to 90010112345. Mieszkam w Warszawie przy ulicy Długiej 5."

static_rules = [
    bank_account.BankAccount,
    name.Name,
    credit_card.CreditCard,
    email.Email,
    pesel_rule.PeselRule,
]

tokens = input.split()
for rule in static_rules:
    tokens = rule.anonymize(tokens)


def mapToString(x) -> str:
    if isinstance(x, str):
        return x
    else:
        return x.label()

print(" ".join(map(mapToString, tokens)))
