from rules.static import bank_account, name, credit_card, email, pesel_rule

input = "Hi, My name is Jan Kowalski. My phone number is +48123123123 and my bank account is PL12345678901234567890123456"

static_rules = [bank_account.BankAccount, name.Name, credit_card.CreditCard, email.Email, pesel_rule.PeselRule]

str = ""
for rule in static_rules:
    input = rule.anonymize(input)

print(input)
