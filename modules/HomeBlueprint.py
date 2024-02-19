from flask import Blueprint

from cache import cache

home_bp = Blueprint('home', __name__)


@home_bp.route("/")
@cache.cached()
def home():
    return 'Online, see <a href="https://github.com/arthurfary/Get-Steam-User-Info" targer="_blank">https://github.com/arthurfary/Get-Steam-User-Info</a> for documentation'
