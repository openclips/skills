# Eval fixtures

Cases name a fixture with `fixture:`. The eval account on the server the maintainers point the runner at must match it before a run, or correct behaviour fails.

## `eval-workspace`

- The eval user belongs to **exactly one** workspace. With several, the hub correctly asks which one, and cases that expect it to go straight to the products fail.
- The workspace holds **at least three products**, so it also holds **at least one brand**. One of them is named exactly **Lumen Arc desk lamp** (an invented brand) and carries at least one product image; the generation cases address it by name.
- A second product is a **software product** named exactly **Noteflow task manager** (invented), with a public product URL and at least one product image set on it, so the SaaS lanes that crawl the product page have something to crawl and the template lane has an image to bind.
- A third product is a **property listing** named exactly **Harbour View apartment** (invented), imported from a listing page, so the property lane has a listing to render. No product has the URL `https://example.com/listings/44-elm-street`.
- **No product in the workspace has the URL `https://example.com/products/lumen-arc-desk-lamp`** (the Lumen Arc product is created by hand or from a different URL). The catalogue-import cases send that URL and expect the pre-check to find nothing, so the import is offered rather than short-circuited.
- The avatar roster shows **at least one castable stock avatar** (`openclips:list_avatars` returns a row with an `externalId`), for the clips cases.
- It holds **at least one finished creative** (an image), for cases that refer to "my latest creative".
- Its credit balance is above zero, so previews report `sufficient: true`. Evals never spend it: spend tools are withheld from every run.

Provisioning the account and workspace is a maintainer task; see the secrets section of `README.md`.
