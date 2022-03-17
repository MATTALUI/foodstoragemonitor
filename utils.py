from datetime import date, timedelta
import config

def get_warning_date():
    return date.today() + timedelta(weeks=config.WARNING_WEEKS)

def get_highlight_date():
    return date.today() + timedelta(weeks=config.HIGHLIGHT_WEEKS)
