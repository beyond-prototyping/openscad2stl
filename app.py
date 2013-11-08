import os
import tempfile

import envoy
from flask import Flask, request, redirect, url_for, Response
from werkzeug import secure_filename


OPENSCAD_BINARY = os.environ['OPENSCAD_BINARY']


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() == 'scad':
            scad_file = tempfile.mktemp('.scad')
            file.save(scad_file)

            stl_file = tempfile.mktemp('.stl')

            try:
                r = envoy.run('{binary} -o {stl_file} {scad_file}'.format(
                    binary=OPENSCAD_BINARY,
                    stl_file=stl_file,
                    scad_file=scad_file
                ))
            except:
                return "Conversion failed, executable not found?", 500

            os.unlink(scad_file)

            if r.status_code == 0:
                resp = Response()
                resp.mimetype = 'application/sla'
                resp.headers['Content-Disposition'] = 'attachment; filename="{0}.stl"'.format(os.path.basename(secure_filename(file.filename)).rsplit('.', 1)[0])
                resp.data = open(stl_file).read()
                os.unlink(stl_file)
                return resp
            else:
                return "Conversion failed with error {0}".format(r.status_code), 500

    return '''<!doctype html>
    <form action="" method=post enctype=multipart/form-data>
      <label for="file">SCAD file:</label>
      <input type="file" name="file" id="file" accept=".scad" placeholder="SCAD file">
      <input type="submit" value="Convert to STL">
    </form>
    '''


if __name__ == "__main__":
    app.run(debug=os.environ.get('DEBUG', False), host='0.0.0.0', port=os.environ.get('PORT', 5000))
