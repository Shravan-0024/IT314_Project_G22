from django.shortcuts import render,redirect
import json
from django.http import JsonResponse, HttpResponseRedirect

def change_theme(request, **kwargs):
    if request.method == 'POST':
        try:
            # Parse incoming data for system preference
            data = json.loads(request.body)
            is_dark_theme = data.get('is_dark_theme', False)  # Default to light mode
            request.session['is_dark_theme'] = is_dark_theme
            return JsonResponse({'message': 'Theme preference set successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    # Handle toggle for manual user input (e.g., from a button)
    if 'is_dark_theme' in request.session:
        request.session['is_dark_theme'] = not request.session.get('is_dark_theme')
    else:
        request.session['is_dark_theme'] = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
