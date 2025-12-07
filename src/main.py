from rules.static import bank_account, name, credit_card, email, pesel_rule, age
import morfeusz2
from flask import Flask, request, jsonify


def mapToString(x) -> str:
    if isinstance(x, str):
        return x
    else:
        return x.label()


def regenerateToken(x) -> str:
    if isinstance(x, str):
        return x
    else:
        return x.generate()


morf = morfeusz2.Morfeusz()
app = Flask(__name__)
static_rules = [
    bank_account.BankAccount,
    name.Name(morf),
    credit_card.CreditCard,
    email.Email,
    pesel_rule.PeselRule,
    age.Age(morf),
]


def anonymize(input: str, regenerate: bool) -> str:
    sentences = input.split(".")
    parsed = []
    # TODO: parallelize each sentence
    for sentence in sentences:
        tokens = sentence.split()
        for rule in static_rules:
            tokens = rule.anonymize(tokens)

        if not regenerate:
            parsed.append(" ".join(map(mapToString, tokens)))
        else:
            parsed.append(" ".join(map(regenerateToken, tokens)))

    return ". ".join(parsed)


@app.route('/api/parse', methods=['POST'])
def parse():
    data = request.get_json(silent=True)
    if data and "text" in data:
        text = data["text"]
    else:
        return jsonify({"error": "invalid request"}), 400

    randomize_flag = request.args.get('randomize', 'false').lower() in ('1', 'true', 'yes')

    result = anonymize(text, randomize_flag)

    return jsonify({
        "anonymized": result,
    })



@app.route("/", methods=["GET"])
def index():
    return """
   <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Anonymizer</title>
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      display: flex;
      flex-direction: column;
      height: 100vh;
    }
    header {
      background: #333;
      color: white;
      padding: 15px;
      text-align: center;
      font-size: 24px;
    }
    .container {
      flex: 1;
      display: flex;
      flex-direction: row;
    }
    textarea {
      width: 50%;
      height: 100%;
      padding: 10px;
      box-sizing: border-box;
      font-size: 16px;
      border: 1px solid #ccc;
      resize: none;
    }
    .controls {
      padding: 10px;
      text-align: center;
    }
    button {
      padding: 10px 20px;
      font-size: 16px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <header>Anonymizer</header>
  <div class="container">
    <textarea id="inputText" placeholder="Enter raw data here..."></textarea>
    <textarea id="outputText" placeholder="Anonymized output will appear here..." readonly></textarea>
  </div>
  <div class="controls">
    <label style="margin-right:10px;">
      <input type="checkbox" id="regenerateFlag"> regenerate
    </label>
    <button onclick="sendData()">Anonymize</button>
  </div>

  <script>
    async function sendData() {
      const text = document.getElementById("inputText").value;
      try {
        const response = await fetch("http://localhost:8000/api/parse" + (document.getElementById("regenerateFlag").checked ? "?regenerate=true" : ""), {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text })
        });
        const json = await response.json();
        document.getElementById("outputText").value = json.anonymized || "";
      } catch (err) {
        document.getElementById("outputText").value = "Error: " + err;
      }
    }
  </script>
</body>
</html>

"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
