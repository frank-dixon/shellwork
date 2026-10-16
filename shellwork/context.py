from .models import Breed


def shellwork(request):
    if not request.path_info.startswith("/shellwork"):
        return {}
    return {"sw_footer_breeds": Breed.objects.filter(published=True).only("name", "slug")}
