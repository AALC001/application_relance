import os
import calendar
import locale
import weasyprint
import activite_relance as ar
from datetime import datetime
from django.http import HttpResponse, Http404
from django.template.loader import get_template, render_to_string
from django.conf import settings

# Export file to pdf
def export_to_pdf(template_src, context_dict={}):
    html_string = render_to_string(template_src, context_dict)
    css = os.path.join(settings.BASE_DIR, 'static/css/report.css')
    html = weasyprint.HTML(string=html_string,)
    return html.write_pdf(stylesheets=[css])

# Download file
def download(request, path, content_type="application/vnd.ms-excel", is_uploaded=False):
    if is_uploaded:
        file_path = os.path.join(settings.BASE_DIR, path)
        filename = "dernier_fichier_patient.xlsx"
    else:
        file_path = os.path.join(settings.STATIC_ROOT, path)
        filename = os.path.basename(file_path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=content_type)
            response['Content-Disposition'] = 'inline; filename=' + filename
            return response
    raise Http404

def get_month_limit(year:int, month:int) -> tuple:
    month_date = []
    cal = calendar.Calendar(0)

    for d in cal.itermonthdates(year, month):
        if d.month == month:
            month_date.append(d)

    return (month_date[0], month_date[-1])
    

def get_year_month() -> list:
    locale.setlocale(locale.LC_TIME, locale='fr_FR.UTF-8')
    return [(i, datetime(2008, i, 1).strftime('%B')) for i in range(1, 13)]

# Check if date in month
def date_in_month(date: datetime, month:str):
    locale.setlocale(locale.LC_TIME, locale='fr_FR.UTF-8')
    if isinstance(date, str):
        return datetime.strptime(date, '%Y-%m-%d').strftime('%B') == month
    else:
        return date.strftime("%B") == month


# Check if date in year
def date_in_year(date: datetime, year: str):
    locale.setlocale(locale.LC_TIME, locale='fr_FR.UTF-8')
    if isinstance(date, str):
        return datetime.strptime(date, '%Y-%m-%d').strftime('%Y') == year
    else:
        return date.strftime("%Y") == year

def get_list_year(min=1, max=9999) -> list:
    return list(range(min, max))


# Convert datetime to be seriazile
def converter(o):
    if isinstance(o, datetime):
        return o.isoformat('/')

    elif isinstance(o, ar.models.Patient):
        return o.__dict__