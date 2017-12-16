from django import template
register = template.Library()


@register.filter
def delta_format(dt):
    if dt is not None:
        import datetime
        time_delta = datetime.datetime.utcnow() - dt.replace(tzinfo=None)
        if time_delta.days == 0:
            days = ""
        elif time_delta.days == 1:
            days = "1 day"
        else:
            days = "%s days" % str(time_delta.days)

        if time_delta.days >= 10:
            return days

        if time_delta.seconds // 3600 > 0:
            hours = str(time_delta.seconds // 3600) + "h"
        else:
            hours = ""

        if time_delta.days >= 1:
            minutes = ""
        else:
            minutes = str(time_delta.seconds % 3600 // 60) + "m"

        return "%s %s %s" % (days, hours, minutes,)
    else:
        return None


egg_flairs = ["lucky", "egg", "eevee", "togepi", "manaphy", "torchic", "pichu", "ditto", "eggcup"]
sp_flairs = ["chatot", "atomic", "totodile", "dragonair", "m-altaria-shiny",
             "jellicent-shiny", "dragonite", "ughhhhhh", "jude", "magnezone-shiny",
             "nsy", "porygon-z-shiny", "porygon", "porygon2", "serperior-shiny",
             "slowpoke", "greninja-shiny", "rod", "mudkip-shiny", "alder", "azumarill-shiny",
             "nidoking", "magikarp-shiny", "kaph", "rhyhorn-shiny"]
ribbon_flairs = ["cuteribbon", "coolribbon", "beautyribbon", "smartribbon", "toughribbon"]


@register.filter
def flair_format(flair_str):
    if flair_str is None or flair_str == "default":
        return ""

    if flair_str in egg_flairs:
        return "egg-flair flair-%s" % flair_str
    elif flair_str in sp_flairs:
        return "sp-flair flair-%s" % flair_str
    elif flair_str in ribbon_flairs:
        return "ribbon-flair flair-%s" % flair_str

    return ""


@register.filter
def gen_format(gen_str):
    if gen_str == '6':
        return "6 (XY/ORAS)"
    elif gen_str == '7':
        return "7 (SM/USUM)"
    else:
        return gen_str


@register.filter
def tsv_url(sub_id, tsv):
    return "https://www.reddit.com/r/SVExchange/comments/%s/%s/" % (sub_id, tsv)


@register.filter
def rdt_search_url(tsv):
    return "https://www.reddit.com/r/SVExchange/search?q=title:%s&restrict_sr=on&sort=new&t=all" % tsv


@register.filter
def as_percentage_of(part, whole):
    try:
        pct = float(part) / whole * 100.0
        return "%.1f" % pct + "%"
    except (ValueError, ZeroDivisionError):
        return ""
