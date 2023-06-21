import re
import typing as t

REGEX_PATTERN = re.compile(
    r"(?:<[^?]+\?(?P<prev>.+)>;\srel=\"prev\"(?:,\s)?)?"
    r"(?:<[^?]+\?(?P<next>.+)>;\srel=\"next\"(?:,\s)?)?"
    r"(?:<.+>;\srel=\"last\"(?:,\s)?)?"
    r"(?:<.+>;\srel=\"first\"(?:,\s)?)?"
)


def build_pagination_links(
    link_header: str, base_url: str
) -> t.Mapping[str, str | None]:
    """
    Build pagination links based in the content of the 'link' header, received
    as response, when invoked the GitHub API's search repositories endpoint.
    """
    match = REGEX_PATTERN.match(link_header)
    if match:
        prev_qs: str | None = match.group("prev")
        next_qs: str | None = match.group("next")
        result = {
            "prev": f"{base_url}?{prev_qs}" if prev_qs else None,
            "next": f"{base_url}?{next_qs}" if next_qs else None,
        }
    else:
        result = {"prev": None, "next": None}

    return result
