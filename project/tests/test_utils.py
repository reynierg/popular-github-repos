import pytest

from app.utils import build_pagination_links

arg_values = [
    (
        "<https://api.github.com/search/repositories?sort=stars&order=desc&per_page=1&q=language%3APython&page=1>"
        "; rel=\"prev\", "
        "<https://api.github.com/search/repositories?sort=stars&order=desc&per_page=1&q=language%3APython&page=3>"
        "; rel=\"next\", "
        "<https://api.github.com/search/repositories?sort=stars&order=desc&per_page=1&q=language%3APython&page=1000>"
        "; rel=\"last\", "
        "<https://api.github.com/search/repositories?sort=stars&order=desc&per_page=1&q=language%3APython&page=1>"
        "; rel=\"first\"",

        {
            "prev": "?sort=stars&order=desc&per_page=1&q=language%3APython&page=1",
            "next": "?sort=stars&order=desc&per_page=1&q=language%3APython&page=3"
        }
    ),
    (
        "<https://api.github.com/search/repositories?sort=stars&order=desc&per_page=1&q=language%3APython&page=1>"
        "; rel=\"prev\", ",

        {"prev": "?sort=stars&order=desc&per_page=1&q=language%3APython&page=1", "next": None}
    ),
    (
        "<https://api.github.com/search/repositories?sort=stars&order=desc&per_page=1&q=language%3APython&page=3>"
        "; rel=\"next\", ",

        {"prev": None, "next": "?sort=stars&order=desc&per_page=1&q=language%3APython&page=3"}
    ),
    (
        "",
        {"prev": None, "next": None}
    ),
]

test_build_navigation_links_tests_ids = [
    "When 'prev' and 'next' are present in the 'link' header",
    "When only 'prev' is present in the 'link' header",
    "When only 'next' is present in the 'link' header",
    "When 'prev' isn't present in the 'link' header, nor is 'next'",
]


@pytest.mark.parametrize("link_header,pagination_links",
                         arg_values,
                         ids=test_build_navigation_links_tests_ids)
def test_build_navigation_links(link_header, pagination_links):
    base_url = ""
    assert build_pagination_links(link_header, base_url) == pagination_links
