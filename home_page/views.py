from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from autoscraper import AutoScraper


def home(request):
    url = 'https://ktu.edu.in/eu/core/announcements.htm'

    try:
        # url = 'https://ktu.edu.in/home.htm'

        wanted_list = ['ANNOUNCEMENTS', 'Dec 24, 2021', 'Exam Registration opened - B.Tech S3 and S5 (supplementary) '
                                                        'Jan 2022']
        scraper = AutoScraper()
        result = scraper.build(url, wanted_list)
        data1 = result[0]
        data2 = result[1]
        data3 = result[2]

        notif = {'data1': data1,
                 'data2': data2,
                 'data3': data3
                 }
        request.session['notif'] = notif
        return render(request, 'index.html', {'notif': notif})

    except:

        notif = {'data1': "KTU site cannot reach"}
        request.session['notif'] = notif
        return render(request, 'index.html', {'notif': notif})
    
