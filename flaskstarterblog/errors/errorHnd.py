from flask import Blueprint , render_template

err_pages = Blueprint('err_pages' , __name__)

@err_pages.app_errorhandler(404)
def err404(error):
        return render_template("404.html"), 404

@err_pages.app_errorhandler(403)
def err403(error):
        return render_template("403.html"), 403