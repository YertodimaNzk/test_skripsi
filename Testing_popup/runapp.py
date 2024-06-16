from flask import Flask, render_template, request

app = Flask(__name__)

diseases = {
    "anemia": {
        "description": "Anemia is a condition in which you lack enough healthy red blood cells to carry adequate oxygen to your body's tissues.",
        "treatment": "Treatment for anemia depends on the cause.",
        "medication": "Iron supplements, Vitamin B12 injections, and Folic acid supplements."
    },
    "diabetes": {
        "description": "Diabetes is a disease that occurs when your blood glucose, also called blood sugar, is too high.",
        "treatment": "Healthy eating, regular exercise, and blood sugar monitoring.",
        "medication": "Insulin therapy, Metformin, and other oral medications."
    }
    # Add more diseases here
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    query = request.args.get('query', '').lower()
    disease = diseases.get(query, None)
    return render_template('result.html', disease=disease, query=query)

if __name__ == '__main__':
    app.run(debug=True)
