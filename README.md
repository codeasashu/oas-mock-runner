## Mock Runner

This uses docs.myoperator.dev as openapi host to run mocks

## Environment vars

You need to set the following env vars to run this app.

**DOCS_ID**: This is the unique identifier of the openapi spec document. 
This has a UUID pattern. You can obtain it by using any document url.

For example, in the url `https://docs.myoperator.dev/openapis/ab3b7fb5-949e-4715-acd7-0fae9e22dc41`
the `ab3b7fb5-949e-4715-acd7-0fae9e22dc41` is the __DOCS_ID__.

**DOCS_AUTH_TOKEN**: Obtain this from Admin panel of docs project.

**DOCS_BASE_URL**: The base url of the docs ui.#

After setting these variables in `.env` file (see `.env.example`), proceed to next
steps.

# Running mocks

Simply run as

```sh
python docker.py
```

This will start a container running the mock of api spec.