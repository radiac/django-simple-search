====================
django-simple-search
==================== 

This application provides a portable, simple way to do search in a Django project.

This fork is a rudimentary packaged version of the application provided by Mike Hostetler:

https://github.com/squarepegsys/django-simple-search

that is based on an article by Julien Phalip:

http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap


Generic search example::

    ### views.py
    from simple_search.utils import generic_search
    from books.models import Author, Book
    from django.shortcuts import render_to_response, redirect


    QUERY = "search-query"

    MODEL_MAP = {
        Author: ["first_name", "last_name", ],
        Book: ["title", "summary"],
    }


    def search(request):
        objects = []
        for model, fields in MODEL_MAP.iteritems():
            objects += generic_search(request, model, fields, QUERY)
        return render_to_response("search_results.html",
                                  {
                                      "objects": objects,
                                      "search_string": request.GET.get(QUERY, ""),
                                  })
