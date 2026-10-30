from flask import render_template
from app.errors import errors_bp

@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html', title='Page Not Found'), 404

@errors_bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html', title='Forbidden'), 403

@errors_bp.app_errorhandler(500)
def internal_error(error):
    # Could rollback database session if an error occurred during commit
    return render_template('errors/500.html', title='Internal Server Error'), 500
