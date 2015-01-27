

def get_profile_picture(backend, user, response, details, is_new=False, *args, **kwargs):
    img_url = None
    if backend.name == 'facebook':
        img_url = 'http://graph.facebook.com/%s/picture?type=large' \
            % response['id']
    elif backend.name == 'twitter':
        img_url = response.get('profile_image_url', '').replace('_normal', '')

    if img_url:
    	user.avatar = img_url
    	user.save()