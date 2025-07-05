from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate_pipeline():
    data = request.get_json()
    description = data.get("description", "")
    mode = data.get("mode", "ollama")

    if not description:
        return jsonify({"error": "Missing 'description' field"}), 400

    try:
        # Crear archivo temporal con la descripción
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as temp_input:
            temp_input.write(description)
            temp_input_path = temp_input.name

        result = subprocess.run(
            ["python3", "lib/pipeline_gen.py", "--mode", mode, "--input", temp_input_path],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "."}
        )

        os.unlink(temp_input_path)

        if result.returncode != 0:
            return jsonify({"error": result.stderr.strip()}), 500

        return jsonify({"result": result.stdout.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
