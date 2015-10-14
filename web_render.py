import web

render = web.template.render("templates")


def render_page(content):
    session = web.config._session
    banner = render.banner(session.loggedin)
    return render.base(session.role, banner, content)
