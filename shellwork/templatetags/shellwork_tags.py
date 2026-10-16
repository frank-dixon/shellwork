from django import template

register = template.Library()


@register.inclusion_tag("shellwork/partials/egg.html")
def css_egg(breed, base=64):
    sd = max(0.0, min(1.0, breed.speckle_density or 0))
    return {"b": breed, "base": base, "sd": sd, "heavy": sd >= 0.5, "k": breed.size_scale}


@register.inclusion_tag("shellwork/partials/egg_pair.html")
def egg_pair(breed, base=64, credit=True):
    return {"b": breed, "base": base, "photo": breed.egg_photo, "credit": credit}


@register.inclusion_tag("shellwork/partials/credit.html")
def credit(photo):
    return {"p": photo}
