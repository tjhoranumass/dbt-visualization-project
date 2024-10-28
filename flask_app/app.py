from flask import Flask, render_template, request
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
import subprocess
import io
import base64

app = Flask(__name__)

db_connection_url = "postgresql://u5h2s7shhkqeo5:pf373bc6d5cddc47f95a938f4914e895c868ca1e01fc5eeb79ad7413b71c6db40@c97r84s7psuajm.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d9snqvovhsjpqs"
engine = create_engine(db_connection_url)

@app.route('/')
def index():
    # Query example: Total Revenue Over Time
    sales_query = """
    SELECT order_date, SUM(total_price) as total_revenue
    FROM stg_sales
    GROUP BY order_date
    ORDER BY order_date;
    """
    sales_data = pd.read_sql(sales_query, engine)

    # Generate a line plot using Plotly
    fig = px.line(sales_data, x='order_date', y='total_revenue', title='Total Revenue Over Time')
    img_html = fig.to_html(full_html=False)

    # Render the home page with the visualization
    return render_template("index.html", img_html=img_html)

@app.route('/product_performance')
def product_performance():
    product_query = """
    SELECT p.product_name, SUM(s.total_price) as total_revenue
    FROM stg_sales s
    JOIN stg_products p ON s.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY total_revenue DESC;
    """
    product_data = pd.read_sql(product_query, engine)

    # Generate a bar chart for product performance
    fig = px.bar(product_data, x='product_name', y='total_revenue', title='Top Products by Revenue')
    img_html = fig.to_html(full_html=False)

    return render_template("index.html", img_html=img_html)

@app.route('/run_pipeline', methods=['POST'])
def run_pipeline():
    try:
        # Run DBT command and capture output
        result = subprocess.run(["dbt", "run"], capture_output=True, text=True, check=True)
        output = result.stdout  # Capture the output to display on the webpage
    except subprocess.CalledProcessError as e:
        output = f"An error occurred: {e.output}"

    # Display the output on the webpage
    return render_template("pipeline_output.html", output=output)


if __name__ == '__main__':
    app.run(debug=True)

