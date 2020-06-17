import os
import pypandoc
from flask import Flask, jsonify, request, send_from_directory, send_file
from io import BytesIO
from docxtpl import DocxTemplate

app = Flask(__name__)
FORMS_FOLDER = os.path.join(app.root_path, "forms")


@app.route('/api/form')
def forms():
    form_list = []
    for f in os.listdir(FORMS_FOLDER):
        if f.endswith('.docx'):
            form_list.append(f)

    return jsonify({
        'forms': form_list
    })


@app.route("/api/form/<name>")
def form(name):
    filename = os.path.join(FORMS_FOLDER, name)
    output = pypandoc.convert_file(filename, "html")
    return jsonify({
        "html": output
    })


@app.route("/api/form/print/<name>")
def print_form(name):
    filename = os.path.join(FORMS_FOLDER, name)
    doc = DocxTemplate(filename)
    doc.render(request.args.to_dict())
    stream = BytesIO()
    doc.get_docx().save(stream)
    stream.seek(0)
    return send_file(stream, mimetype='docx')


if __name__ == '__main__':
    app.run(debug=True)
