from sv import natures
import re

nat_re = re.compile(r"[(]*(\d,\d|\d)[)]* [|-] \w+([-'’]\w+)* (\w+ )*([(].[)] )*[|-] (?P<nat>\w+)", re.UNICODE)

six_iv = re.compile(r"3[01][./]3[01][./]3[01][./]3[01][./]3[01][./]3[01]")
no_atk = re.compile(r"3[01][./]\d{1,2}[./]3[01][./]3[01][./]3[01][./]3[01]")
no_def = re.compile(r"3[01][./]3[01][./]\d{1,2}[./]3[01][./]3[01][./]3[01]")
no_spa = re.compile(r"3[01][./]3[01][./]3[01][./]\d{1,2}[./]3[01][./]3[01]")
no_spdf = re.compile(r"3[01][./]3[01][./]3[01][./]3[01][./]\d{1,2}[./]3[01]")
no_spee = re.compile(r"3[01][./]3[01][./]3[01][./]3[01][./]3[01][./]\d{1,2}")


def is_perfect(line):
    six = six_iv.search(line)
    if six:  # 6 iv = perfect no matter what
        return True

    m = nat_re.search(line)
    if m:  # verify that the line contains a nature
        nature = m.group('nat')
    else:
        return False

    #if nature in natures.lonely: 6iv spreads are commented out
    #    return bool(no_def.search(line))
    if nature in natures.brave:
        return bool(no_spee.search(line))
    elif nature in natures.adamant:
        return bool(no_spa.search(line))
    #elif nature in natures.naughty:
    #    return bool(no_spdf.search(line))
    elif nature in natures.bold:
        return bool(no_atk.search(line))
    elif nature in natures.relaxed:
        return bool(no_spee.search(line))
    elif nature in natures.impish:
        return bool(no_spa.search(line))
    #elif nature in natures.lax:
    #    return bool(no_spdf.search(line))
    elif nature in natures.timid:
        return bool(no_atk.search(line))
    #elif nature in natures.hasty:
    #    return bool(no_def.search(line))
    elif nature in natures.jolly:
        return bool(no_spa.search(line))
    #elif nature == "Naive":
    #    return bool(no_spdf.search(line))
    elif nature in natures.modest:
        return bool(no_atk.search(line))
    #elif nature in natures.mild:
    #    return bool(no_def.search(line))
    elif nature in natures.quiet:
        return bool(no_spee.search(line))
    #elif nature in natures.rash:
    #    return bool(no_spdf.search(line))
    elif nature in natures.calm:
        return bool(no_atk.search(line))
    #elif nature in natures.gentle:
    #    return bool(no_def.search(line))
    elif nature in natures.sassy:
        return bool(no_spee.search(line))
    elif nature in natures.careful:
        return bool(no_spa.search(line))
    else:
        return False
