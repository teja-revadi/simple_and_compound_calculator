from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, request, send_file, session
from datetime import datetime, timedelta
import calendar
from html_generator import create_html_file

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def helper_simple_interest(principal_amount, rate_of_interest, start_date_str, end_date_str ):
    date_format = "%d-%m-%Y"

    start_date = datetime.strptime(start_date_str, date_format).date()
    end_date = datetime.strptime(end_date_str, date_format).date()

    interest_array = []
    total_interest = 0
    S_No = 0
    while start_date.year != end_date.year or start_date.month != end_date.month:
        if start_date.day != 1:
            no_of_days = calendar.monthrange(start_date.year, start_date.month)[1] - start_date.day
            current_month_interest = round(principal_amount * rate_of_interest * no_of_days / (30 * 100), 2)
            total_interest += current_month_interest
            S_No += 1
            month_name = calendar.month_name[start_date.month]
            interest_array.append([S_No, month_name, start_date.year, current_month_interest, total_interest])
            start_date += timedelta(days=no_of_days + 1)
        else:
            current_month_interest = round(principal_amount * rate_of_interest / 100, 2)
            total_interest += current_month_interest
            S_No += 1
            month_name = calendar.month_name[start_date.month]
            interest_array.append([S_No, month_name, start_date.year, current_month_interest, total_interest])
            start_date += relativedelta(months=1)

    # Calculate the interest for the last month
    no_of_days = end_date.day - 1
    last_month_interest = round(principal_amount * rate_of_interest * no_of_days / (30 * 100), 2)
    total_interest += last_month_interest
    S_No += 1
    month_name = calendar.month_name[start_date.month]
    interest_array.append([S_No, month_name, start_date.year, last_month_interest, total_interest])
    return interest_array


def helper_compound_interest(principal_amount, rate_of_interest, start_date_str, end_date_str):
    date_format = "%d-%m-%Y"

    start_date = datetime.strptime(start_date_str, date_format).date()
    end_date = datetime.strptime(end_date_str, date_format).date()

    interest_array = []
    total_interest = 0
    S_No = 0

    while start_date.year != end_date.year or start_date.month != end_date.month:
        if start_date.day != 1:
            no_of_days = calendar.monthrange(start_date.year, start_date.month)[1] - start_date.day
            current_month_interest = round(principal_amount * rate_of_interest * no_of_days / (30 * 100), 2)
            total_interest = round(current_month_interest + total_interest, 2)
            S_No += 1
            if S_No % 12 == 0:
                principal_amount = round(principal_amount + total_interest, 2)
            month_name = calendar.month_name[start_date.month]
            interest_array.append([S_No, month_name, start_date.year, current_month_interest, total_interest])
            start_date += timedelta(days=no_of_days + 1)
        else:
            current_month_interest = round(principal_amount * rate_of_interest / 100, 2)
            total_interest = round(current_month_interest + total_interest, 2)
            S_No += 1
            if S_No % 12 == 0:
                principal_amount = round(principal_amount + total_interest, 2)
            month_name = calendar.month_name[start_date.month]
            interest_array.append([S_No, month_name, start_date.year, current_month_interest, total_interest])
            start_date += relativedelta(months=1)

    # Calculate the interest for the last month
    no_of_days = end_date.day - 1
    last_month_interest = round(principal_amount * rate_of_interest * no_of_days / (30 * 100), 2)
    total_interest += last_month_interest
    S_No += 1
    month_name = calendar.month_name[start_date.month]
    interest_array.append([S_No, month_name, start_date.year, last_month_interest, total_interest])
    return interest_array




@app.route('/')
def index():
    return render_template('loan_calculator.html')


@app.route('/download_pdf')
def download_pdf():
    principal_amount = float(request.args.get("principal_amount"))
    rate_of_interest = float(request.args.get("rate_of_interest"))
    start_date_str = request.args.get("start_date_str")
    end_date_str = request.args.get("end_date_str")
    create_html_file(helper_simple_interest(principal_amount, rate_of_interest, start_date_str, end_date_str),'output.pdf')
    pdf_file_path = 'output.pdf'

    # Provide a custom filename for the downloaded file
    custom_filename = 'Simple-Interest.pdf'

    # Create a file response and specify the MIME type
    return send_file(pdf_file_path, as_attachment=True, download_name=custom_filename)

@app.route('/download_compound_pdf')
def download_compound_pdf():
    principal_amount = float(request.args.get("principal_amount"))
    rate_of_interest = float(request.args.get("rate_of_interest"))
    start_date_str = request.args.get("start_date_str")
    end_date_str = request.args.get("end_date_str")
    create_html_file(helper_simple_interest(principal_amount, rate_of_interest, start_date_str, end_date_str),
                     'output_compound.pdf')
    pdf_file_path = 'output_compound.pdf'

    # Provide a custom filename for the downloaded file
    custom_filename = 'Compound-Interest.pdf'

    # Create a file response and specify the MIME type
    return send_file(pdf_file_path, as_attachment=True, download_name=custom_filename)



@app.route('/simple_interest', methods=['POST'])
def calculate_loan():
    principal_amount = float(request.form['principal_amount'])
    rate_of_interest = float(request.form['rate_of_interest'])
    start_date_str = request.form['start_date']
    end_date_str = request.form['end_date']
    interest_array = helper_simple_interest(principal_amount, rate_of_interest, start_date_str, end_date_str )

    return render_template('loan_results.html', interest_array=interest_array, principal_amount=principal_amount, rate_of_interest=rate_of_interest, start_date_str=start_date_str, end_date_str=end_date_str  )

@app.route('/compound_interest', methods=['POST'])
def calculate_loan_compound():
    principal_amount = float(request.form['principal_amount'])
    rate_of_interest = float(request.form['rate_of_interest'])
    start_date_str = request.form['start_date']
    end_date_str = request.form['end_date']
    interest_array = helper_compound_interest(principal_amount, rate_of_interest, start_date_str, end_date_str )

    return render_template('loan_compound_results.html', interest_array=interest_array, principal_amount=principal_amount, rate_of_interest=rate_of_interest, start_date_str=start_date_str, end_date_str=end_date_str  )

if __name__ == '__main__':
    app.run(debug=True)








