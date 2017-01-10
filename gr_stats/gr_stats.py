from flask import Flask, render_template, request
import data_builder
import pygal
import calendar

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view_stats', methods=['POST'])
def view_stats():
    db = data_builder.DataBuilder(request.form['user_id'])
    try:
        db.fetch()
    except data_builder.ForbiddenError:
        return render_template('forbidden.html')
    except data_builder.NotFoundError:
        return render_template('not_found.html', user_id=request.form['user_id'])


    pages_chart = pygal.Bar(width=800, height=400, explicit_size=True,
        title="Total pages per month", disable_xml_declaration=True)
    pages_chart.x_labels = calendar.month_abbr[1:]
    pages_chart.add("Pages read", db.page_histogram)
    
    books_chart = pygal.Bar(width=800, height=400, explicit_size=True,
        title="Total books per month", disable_xml_declaration=True)
    books_chart.x_labels = calendar.month_abbr[1:]
    books_chart.add("Books read", db.book_histogram)

    return render_template('view_stats.html', pages_chart=pages_chart,
        books_chart=books_chart)

