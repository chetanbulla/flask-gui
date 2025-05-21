from flask import Flask, render_template, request
import os
import csv
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    file_content = ''
    table_data = None

    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = file.filename.lower()
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                if filename.endswith('.csv'):
                    with open(filepath, newline='', encoding='utf-8-sig') as f:
                        sample = f.read(1024)
                        f.seek(0)
                        try:
                            dialect = csv.Sniffer().sniff(sample)
                        except csv.Error:
                            dialect = csv.excel
                        reader = csv.reader(f, dialect)
                        table_data = list(reader)

                elif filename.endswith('.xlsx'):
                    df = pd.read_excel(filepath)
                    table_data = df.values.tolist()
                    table_data.insert(0, df.columns.tolist())  # Add headers as first row

                else:  # Assume plain text
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()

            except Exception as e:
                file_content = f"Error reading file: {str(e)}"

    return render_template('index.html', content=file_content, table=table_data)


if __name__ == '__main__':
    app.run(debug=True)