from flask import Flask, render_template, request
import itertools

app = Flask(__name__)

def generate(query:str):
    if len(query) < 3:
        raise Exception("Expression is very small")
    elements = sorted(set(filter(str.isalpha, query)))
    if len(elements) < 2:
        raise Exception("Less that 2 variables")
    if len(elements) > 5:
        raise Exception("More that 5 variables")
    combinations = list(itertools.product([0, 1], repeat=len(elements)))
    try:
        result = [combo + (eval(query, {}, dict(zip(elements, combo))), ) for combo in combinations]
    except Exception as e:
        raise Exception("Error parsing query")
    return (elements, result)

@app.route("/", methods=['POST','GET'])
def home():
    if request.method == "POST":
        expression = str(request.form['expression'])
        try:
            elements, result = generate(expression)
            return render_template('index.html', table=1, elements=elements, result=result)
        except:
            return render_template('index.html', table=0)
    return render_template('index.html', table=0)

if __name__ == "__main__":
    app.run()