import web
from web_render import render, render_page
from menu import get_menu_items
from db import db

def make_waiter_page(message = None):
    mitems = get_menu_items()
    alerts = get_alerts()
    page = render.waiter_banner(mlist = mitems, message = message, alerts = alerts)
    return render_page(page)

def get_alerts():
    session = web.config._session
    params = dict( wid = session.userid , ts = "datetime('now')")
    alerts = db.select('Alerts JOIN Orders', vars=params,
            where='waiter=$wid and stime<= datetime("now")').list()
    print alerts
    update_query = """
    update Alerts set stime=datetime('now', '+10 minutes')
    where exists (select Alerts.id as aid from Alerts JOIN Orders
    where waiter=$wid and stime<= $ts)
    """
    db.query(update_query, vars=params)
    return alerts
