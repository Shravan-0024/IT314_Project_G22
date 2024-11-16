def theme(request):
    if 'is_dark_theme' in request.session:
        is_dark_theme = request.session.get('is_dark_theme')
    else:
        # Check for system preference (requires JavaScript detection)
        # Default to `False` for safety if no client-side preference is provided
        is_dark_theme = False  # Default value if system preference is unknown
    return {'is_dark_theme': is_dark_theme}
