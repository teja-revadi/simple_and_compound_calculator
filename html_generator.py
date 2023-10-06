from weasyprint import HTML


def create_html_file(interest_array,dir):
    # the html code which will go in the file GFG.html
    html_template = """<html>
    <head>
    <title>Title</title>
    <style>
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 50%;
    }
    
    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }
    
    tr:nth-child(even) {
      background-color: #dddddd;
    }
    </style>
    </head>
    <body>
    <h2>Simple interest Calculator</h2>
    <table>
    """

    html_template += """
      <tr>
        <th>S.No</th>
        <th>Month</th>
        <th>Year </th>
        <th>Interest for current month</th>
        <th>Total Interest</th>
      </tr>
    """
    for month in interest_array:
        html_template += f"""
        <tr>

        <td>{month[0]}</td>
        <td>{month[1]} </td>
        <td>{month[2]}</td>
        <td>{month[3]}</td>
        <td>{month[4]}</td>
        </tr>
        
        """

    html_template += """
    </table>
        
    </body>
    </html>
    """

    HTML(string=html_template).write_pdf(dir)

