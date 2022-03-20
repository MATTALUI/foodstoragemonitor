from flask import Blueprint
from datetime import date, datetime
import json

from models import ItemSet
from utils import get_warning_date, get_highlight_date
from hardware_manager import hardware_manager

cron_blueprint = Blueprint('cron_blueprint', __name__)

###############################################################################
# CRON ROUTES
###############################################################################
@cron_blueprint.route("/cron/test/", methods=['POST'])
def test_cron():
    hardware_manager.run_test()
    return "All's well!\n"

@cron_blueprint.route("/cron/check-expiry/", methods=['POST'])
def check_expiry():
    report = build_expiry_report()
    write_expiry_report(report)
    hardware_manager.accept_report(report)

    return json.dumps(report) + "\n"

def build_expiry_report():
    expired_items = ItemSet.query.filter(ItemSet.expiration < date.today()).count()
    warning_items = ItemSet.query.filter(ItemSet.expiration < get_warning_date()).filter(ItemSet.expiration >= date.today()).count()
    highlight_items = ItemSet.query.filter(ItemSet.expiration < get_highlight_date()).filter(ItemSet.expiration >= get_warning_date()).count()

    return {
        "expired": expired_items,
        "warning": warning_items,
        "highlight": highlight_items,
    }

def write_expiry_report(report):
    expired_padding = " " * (19 - len(str(report["expired"])))
    warning_padding = " " * (19 - len(str(report["warning"])))
    highlight_padding = " " * (17 - len(str(report["highlight"])))
    report_file = open("report.txt", "w")
    report_file.write("▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜" + "\n")
    report_file.write("▌ " + str(datetime.now()) + "  ▐\n")
    report_file.write("▌ expired: " + str(report["expired"]) + expired_padding + "▐\n")
    report_file.write("▌ warning: " + str(report["warning"]) + warning_padding + "▐\n")
    report_file.write("▌ highlight: " + str(report["highlight"]) + highlight_padding + "▐\n")
    report_file.write("▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟" + "\n")
    report_file.close()
