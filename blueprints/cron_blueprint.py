from flask import Blueprint
from datetime import date, datetime
import json

import config
from models import ItemSet, Category
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

@cron_blueprint.route("/cron/reset/", methods=['GET', 'POST'])
def reset():
    hardware_manager.reset()
    return 'true'

@cron_blueprint.route("/cron/check-expiry/", methods=['POST'])
def check_expiry():
    report = build_expiry_report()
    write_expiry_report(report)
    hardware_manager.accept_report(report)

    return json.dumps(report) + "\n"

@cron_blueprint.route("/cron/check-longevity/", methods=['POST'])
def check_longevity():
    items = ItemSet.query.all()
    edible_count = 0
    drinkable_count = 0
    consumption_rate = config.FAMILY_MEMBER_COUNT * config.MEALS_PER_DAY_COUNT

    for item in items:
        if item.is_drinkable:
            drinkable_count += item.quantity
        else:
            edible_count += item.quantity

    edible_longevity = edible_count / consumption_rate
    drinkable_longevity = drinkable_count / consumption_rate

    return json.dumps({
        "drinkable_count": drinkable_count,
        "edible_count": edible_count,
        "consumption_rate": consumption_rate,
        "edible_longevity": edible_longevity,
        "drinkable_longevity": drinkable_longevity,
    }) + "\n"

def count_nonexpired(items):
    count = 0
    for item in items:
        if not item.is_ignorable:
            count += 1
    return count

def build_expiry_report():
    expired_items = ItemSet.query.filter(ItemSet.expiration < date.today()).all()
    warning_items = ItemSet.query.filter(ItemSet.expiration < get_warning_date()).filter(ItemSet.expiration >= date.today()).all()
    highlight_items = ItemSet.query.filter(ItemSet.expiration < get_highlight_date()).filter(ItemSet.expiration >= get_warning_date()).all()

    return {
        "expired": count_nonexpired(expired_items),
        "warning": count_nonexpired(warning_items),
        "highlight": count_nonexpired(highlight_items),
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
