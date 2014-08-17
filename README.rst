====================
django-simple-search
==================== 

This application provides a portable, simple way to do search in a Django project.

This fork is a rudimentary packaged version of the application provided by Mike Hostetler:

https://github.com/squarepegsys/django-simple-search

that is based on an article by Julien Phalip:

http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap


Usage
=====

At the top of your view, import the ``simple_search`` search module. It exposes
two functions:

``simple_search.generic_search(request, model, fields, query_param)``
    This takes 3 arguments (``query_param`` is optional) and returns a queryset
    of search results. It is the easiest way to perform a search.
    
    Arguments:
        ``request``
            The request object, as passed to your view.
            
        ``model``
            The model or queryset to search. A model will be converted to a
            queryset by using ``model.objects.all()``
        
        ``fields``
            A list of fields to search in the model.
        
        ``query_param`` (optional)
            The name of the GET parameter which contains the search string.
            
            Default: ``q``
    
    Returns:
        ``queryset``
            The queryset containing the results. If the search string was
            empty, the original queryset (or all objects) will be returned.

``simple_search.perform_search(query_string, model, fields)``
    This takes 3 arguments and returns a queryset of search results.
    
    Use this function if you want to use the stripped search query string
    elsewhere in your view.
    
    Arguments:
        ``query_string``
            The string to search the model for. You should call ``strip()`` on
            it before passing it to the function.
            
            Example: 
                query_string = request.GET.get("q", "").strip()
        
        ``model``
            The model or queryset to search. A model will be converted to a
            queryset by using ``model.objects.all()``
        
        ``fields``
            A list of fields to search in the model.
        
    Returns:
        ``queryset``
            The queryset containing the results. If the search string was
            empty, the original queryset (or all objects) will be returned.


Example
=======

Generic search example::

    ### views.py
    from simple_search import generic_search, perform_search
    from books.models import Author, Book
    from django.shortcuts import render_to_response, redirect, get_object_or_404


    QUERY = "search-query"

    MODEL_MAP = {
        Author: ["first_name", "last_name", ],
        Book: ["title", "summary"],
    }


    def search(request):
        """Search Author and Book"""
        objects = []
        for model, fields in MODEL_MAP.iteritems():
            objects += generic_search(request, model, fields, QUERY)
            
        return render_to_response("search_results.html",
                                  {
                                      "objects": objects,
                                      "search_string": request.GET.get(QUERY, ""),
                                  })

    def list_books(request, author_pk):
        """List books by a specific author, with optional search"""
        query_string = request.GET.get(QUERY, "").strip()
        author = get_object_or_404(Author, pk=author_pk)
        books = Books.objects.filter(author=author)
        books = perform_search(query_string, books, MODEL_MAP['Book'])
        
        return render_to_response("list_books.html",
                                  {
                                      "books": books,
                                      "search_string": query_string,
                                  })
