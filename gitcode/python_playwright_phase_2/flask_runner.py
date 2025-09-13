from flask import Flask, request, jsonify
from dotenv import load_dotenv
from index import run_automation
import asyncio


load_dotenv()

app = Flask(__name__)


@app.route("/run-robot", methods=["POST"])
def run_robot():
    try:
        data = request.json
        excel_file_path = data.get("excel_file_path")
        env = data.get("env")
        user_id = data.get("user_id")

        print("Starting automation...")
        asyncio.run(run_automation(excel_file_path, env, user_id))
        print("Automation completed.")

        return jsonify({"message": "Automation completed successfully."}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3003, debug=True)
