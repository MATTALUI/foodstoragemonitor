from flask import Blueprint
from datetime import date, datetime
import json

from models import ItemSet
from utils import get_warning_date, get_highlight_date

cron_blueprint = Blueprint('cron_blueprint', __name__)

###############################################################################
# CRON ROUTES
###############################################################################
@cron_blueprint.route("/cron/test", methods=['POST'])
def test_cron():
    return "All's well!"

@cron_blueprint.route("/cron/check-expiry", methods=['POST'])
def check_expiry():
    expired_items = ItemSet.query.filter(ItemSet.expiration < date.today()).count()
    warning_items = ItemSet.query.filter(ItemSet.expiration < get_warning_date()).filter(ItemSet.expiration >= date.today()).count()
    highlight_items = ItemSet.query.filter(ItemSet.expiration < get_highlight_date()).filter(ItemSet.expiration >= get_warning_date()).count()

    report = open("report.txt", "w")
    report.write("▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜" + "\n")
    report.write("▌ " + str(datetime.now()) + "\n")
    report.write("▌ expired:" + str(expired_items) + "\n")
    report.write("▌ warning:" + str(warning_items) + "\n")
    report.write("▌ highlight:" + str(highlight_items) + "\n")
    report.write("▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟" + "\n")
    report.close()

    return json.dumps({
        "expired": expired_items,
        "warning": warning_items,
        "highlight": highlight_items,
    })
