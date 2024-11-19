def theme(request):
    if 'is_dark_theme' in request.session:
        is_dark_theme = request.session.get('is_dark_theme')
    else:
        # Default to system preference
        is_dark_theme = request.COOKIES.get('system_dark_theme', 'false') == 'true'
    return {'is_dark_theme': is_dark_theme}
