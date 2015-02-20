Contact endpoint
================

Endpoint for contact search. Follows specification of Moxie.

.. http:get:: /contact/search

    Search for persons by name and medium (tel or email)

    **Example request**:

    .. sourcecode:: http

		GET /contact/search?q=smith&medium=phone&match=exact HTTP/1.1
		Host: api.m.ox.ac.uk
		Accept: application/json

    **Example response as HAL/JSON**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
          "_links": {
            "self": {
              "href": "/contact/search?q=martin&medium=phone&match=exact"
            }
          },
          "persons": [
            {
              "external_tel": "xxxxx xxxxx",
              "internal_tel": "xxxxx",
              "name": "Martin, Dr X",
              "unit": "X, Department of"
            },
            {
              "external_tel": "xxxxx xxxxx",
              "internal_tel": "xxxxx",
              "name": "Martin, Dr X",
              "unit": "X"
            },
            [...]
          ]
        }

    The response contains a list of results. 

    :query q: search query
    :type q: string
    :query medium: directory to search: `phone` or `email`
    :type medium: string
    :query match: which entries to match: `exact` or `approximate`
    :type match: string

    :statuscode 200: results found
    :statuscode 400: search query is inconsistent (expect details about the error as application/json in the body of the response)
    :statuscode 503: search service is not available
