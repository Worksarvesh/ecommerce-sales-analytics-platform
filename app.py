from io import StringIO

from flask import Flask, Response, jsonify, render_template
from werkzeug.exceptions import HTTPException

from config import config
from scripts.analytics import (
    export_powerbi_dataframe,
    get_average_order_value,
    get_best_customers,
    get_country_sales,
    get_customer_ranking,
    get_monthly_sales,
    get_top_products,
    get_total_sales,
)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.secret_key

    @app.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, HTTPException):
            return jsonify({"error": error.name, "message": error.description}), error.code
        app.logger.exception("Unhandled application error")
        return jsonify({"error": "Application error", "message": str(error)}), 500

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/api/total-sales")
    def api_total_sales():
        return jsonify(get_total_sales())

    @app.route("/api/monthly-sales")
    def api_monthly_sales():
        return jsonify(get_monthly_sales())

    @app.route("/api/top-products")
    def api_top_products():
        return jsonify(get_top_products())

    @app.route("/api/country-sales")
    def api_country_sales():
        return jsonify(get_country_sales())

    @app.route("/api/best-customers")
    def api_best_customers():
        return jsonify(get_best_customers())

    @app.route("/api/average-order-value")
    def api_average_order_value():
        return jsonify(get_average_order_value())

    @app.route("/api/customer-ranking")
    def api_customer_ranking():
        return jsonify(get_customer_ranking(limit=50))

    @app.route("/api/export-csv")
    def api_export_csv():
        output = StringIO()
        export_powerbi_dataframe().to_csv(output, index=False)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=ecommerce_powerbi_export.csv"},
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=config.debug)
