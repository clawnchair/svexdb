from django.core.cache import cache
from django.shortcuts import render
from ratelimit.decorators import ratelimit
from sv.models import TSV
from sv.forms import DumpForm
from sv import dump_search


def brb(request):
    from django.http import HttpResponse
    return HttpResponse('Undergoing maintenance<br> Be back later<br>Sorry for any inconvenience.')


# @ratelimit(key='header:x-forwarded-for', block=True, rate='5/3s') # prod
# @ratelimit(key='ip', block=True, rate='5/3s') # local
def paste(request):
    error = False
    if request.method == 'GET':
        paste_form = DumpForm()
    else:
        # A POST request: Handle Form Upload
        paste_form = DumpForm(request.POST)  # Bind data from request.POST into a PostForm

        # If data is valid, proceeds to create a new post and redirect the user
        if paste_form.is_valid():
            text = paste_form.cleaned_data['paste']
            gen = paste_form.cleaned_data['gen_choice']
            '''if gen is '7':
                flag = False
            else:
                flag = paste_form.cleaned_data['include_nonreddit']'''
            flag = False

            ds = dump_search.DumpSearcher(text, flag, gen)
            d = ds.process_text()

            return render(request, 'result.html', {'item_list': d['results'],
                                                   'total': d['total'],
                                                   'unique': d['unique'],
                                                   'exceeded': d['exceeded'],
                                                   'multiples': d['multi'],
                                                   'nonreddit': d['nonreddit'],
                                                   'gen': gen})
    u6 = cache.get('u6', TSV.objects.get_unique_count('6'))
    u7 = cache.get('u7', TSV.objects.get_unique_count('7'))
    return render(request, 'dump_form.html', {'error': error,
                                              'paste_area': paste_form,
                                              'uniques6': u6,
                                              'uniques7': u7, })


def esv_tabler(request):
    return render(request, 'esv_tabler.html')
