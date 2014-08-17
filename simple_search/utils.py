import re
import operator

try:
    from functools import reduce
except ImportError:
    # In Python 2 reduce is in builtins
    pass

from django.db.models import Q, query


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    """
    Splits the query string in invidual keywords, getting rid of unecessary
    spaces and grouping quoted words together.
    Example:
    
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
    ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    """
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def build_query(query_string, search_fields):
    """
    Returns a query, that is a combination of Q objects. That combination
    aims to search keywords within a model by testing the given search fields.
    """
    terms = normalize_query(query_string)

    if not terms:
        return None

    query = reduce(
        operator.__and__,
        (reduce(
            operator.__or__,
            (Q(**{"%s__icontains" % field_name: term}) for field_name in search_fields)
        ) for term in terms),
    )
    return query


def perform_search(query_string, model, fields):
    """
    Perform a search in the given fields of a model or queryset
    """
    # Ensure we're dealing with a queryset
    queryset = model
    if not isinstance(queryset, query.QuerySet):
        queryset = model.objects.all()
    
    if not query_string:
        return queryset
    
    entry_query = build_query(query_string, fields)
    return queryset.filter(entry_query)


def generic_search(request, model, fields, query_param="q"):
    """
    Look up a search string in the request GET, and perform a search in the
    given fields of a model or queryset
    """
    query_string = request.GET.get(query_param, "").strip()
    return perform_search(query_string, model, fields)
