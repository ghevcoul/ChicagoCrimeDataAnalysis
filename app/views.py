from io import BytesIO

from flask import render_template, session, make_response
from sqlalchemy import func
import pandas as pd
import seaborn as sns

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

from app import app, db
from .models import Chicago

@app.route('/')
def home():
    df = pd.DataFrame(db.session.query(Chicago.date, func.count(Chicago.primary_type)).group_by(Chicago.date).order_by(Chicago.date).all(), columns=["Date", "Count"])

    fig = Figure()
    ax = fig.add_subplot(111)
    x = df["Date"]
    y = df["Count"]
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers["Content-Type"] = "image/png"
    return response