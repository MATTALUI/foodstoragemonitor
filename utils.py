from datetime import date, timedelta
import config

def get_warning_date():
    return date.today() + timedelta(weeks=config.WARNING_WEEKS)

def get_highlight_date():
    return date.today() + timedelta(weeks=config.HIGHLIGHT_WEEKS)

def build_sortable_column(key, params):
    sort = params.get("sort")
    order = params.get("order")
    addtl_query = ""
    asc_suffix = 's' if sort == key and order == 'asc' else 'r'
    desc_suffix = 's' if sort == key and order == 'desc' else 'r'
    for param in params:
        if param in ['sort', 'order']:
            continue
        value = params[param]
        addtl_query += f"&{param}={value}"

    return f"""
        <span class="d-flex">
            {key.capitalize()}
            <div class="d-flex align-items-center ml-1">
                <a href="?sort={key}&order=asc{addtl_query}" class="clickable sorter ml-1"><i class="fa{asc_suffix} fa-caret-circle-up"></i></a>
                <a href="?sort={key}&order=desc{addtl_query}" class="clickable sorter ml-1"><i class="fa{desc_suffix} fa-caret-circle-down"></i></a>
            </div>
        </span>
    """
