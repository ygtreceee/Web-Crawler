from flask import Flask, render_template
import get_data

app = Flask(__name__)
spider = get_data.mySpider()


@app.route('/')
def index():
    one_month_data = spider.get_one_month()
    three_month_data = spider.get_three_month()
    three_year_data = spider.get_three_year()
    one_year_picture = spider.one_year_picture()

    return render_template('index.html',
                           one_month_data=one_month_data,
                           three_month_data=three_month_data,
                           three_year_data=three_year_data,
                           one_year_picture=one_year_picture)


if __name__ == '__main__':
    app.run()
