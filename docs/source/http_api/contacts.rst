Contact endpoint
================

Endpoint for contact searcg. Follows specification of Moxie.

.. http:get:: /contact/search

    Search for persons by name and medium (tel or email)

    **Example request**:

    .. sourcecode:: http

		GET /contact/search?q=smith HTTP/1.1
		Host: api.m.ox.ac.uk
		Accept: application/hal+json

    **Example response as HAL+JSON**:

    .. sourcecode:: http

		HTTP/1.1 200 OK
		Content-Type: application/hal+json


    The response contains a list of results, links to go to first, previous, next and last pages depending on current `start` and `count` parameters, and the total count of results.

    :query q: title to search for
    :type q: string
    :query medium: author to search for
    :type medium: string

    :statuscode 200: results found
    :statuscode 400: search query is inconsistent (expect details about the error as plain/text in the body of the response)
    :statuscode 503: search service is not available
