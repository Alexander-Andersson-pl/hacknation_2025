from rules.static import bank_account, name, credit_card, email, pesel_rule
from src.rules.static import age
import morfeusz2
from flask import Flask, request, jsonify

morf = morfeusz2.Morfeusz()

def mapToString(x) -> str:
    if isinstance(x, str):
        return x
    else:
        return x.label()

input = "Nazywam się Jan Kowalski, mój PESEL to 87091118526. Mieszkam w Warszawie przy ulicy Długiej 5. Lubię Warszawę. Miałem 5 lat. Mieszkam w domu. Mieszkam w Warszawie."

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
    for sentence in sentences:
        tokens = sentence.split()
        for rule in static_rules:
            tokens = rule.anonymize(tokens)

        parsed.append(" ".join(map(mapToString, tokens)))

    return ".".join(parsed)



app = Flask(__name__)

@app.route('/api/parse', methods=['POST'])
def parse():
    data = request.get_json(silent=True)
    if data and "text" in data:
        text = data["text"]
    else:
        # fallback: raw body as text
        text = request.data.decode('utf-8')

    # 2. Get 'randomize' flag from query param, default False
    randomize_flag = request.args.get('randomize', 'false').lower() in ('1','true','yes')

    # 3. Process
    result = anonymize(text, randomize_flag)

    # 4. Return JSON
    return jsonify({
        "original": text,
        "anonymized": result,
        "randomize": randomize_flag
    })

@app.route('/', methods=['GET'])
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
    <button onclick="sendData()">Anonymize</button>
  </div>

  <script>
    async function sendData() {
      const text = document.getElementById("inputText").value;
      try {
        const response = await fetch("http://localhost:8000/api/parse", {
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
    app.run(host='0.0.0.0', port=8000, debug=True)