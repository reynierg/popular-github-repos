import random
import string

import factory
from factory import fuzzy

LICENSES_METADATA = {
    "apache-2.0": {
        "name": "Apache License 2.0",
        "spdx_id": "Apache-2.0"
    },
    "mit": {
        "name": "MIT License",
        "spdx_id": "MIT"
    },
    "gpl-2.0": {
        "name": "GNU General Public License v2.0",
        "spdx_id": "GPL-2.0"
    },
    "gpl-3.0": {
        "name": "GNU General Public License v3.0",
        "spdx_id": "GPL-3.0"
    },
    "agpl-3.0": {
        "name": "GNU Affero General Public License v3.0",
        "spdx_id": "AGPL-3.0"
    },
    "bsd-3-clause": {
        "name": "BSD 3-Clause \"New\" or \"Revised\" License",
        "spdx_id": "BSD-3-Clause"
    },
    "bsd-4-clause": {
        "name": "BSD 4-Clause \"Original\" or \"Old\" License",
        "spdx_id": "BSD-4-Clause"
    },
    "other": {
        "name": "Other",
        "spdx_id": "NOASSERTION"
    }
}

PROGRAMMING_LANGUAGES = [
    "Python",
    "Go",
    "JavaScript",
    "PHP",
    "TypeScript",
    "Assembly",
    "HTML",
    "R",
    "Objective-C",
    "Swift",
    "Shell",
    "Vue",
    None,
]


class OwnerFactory(factory.DictFactory):
    id = fuzzy.FuzzyText(chars=string.digits, length=4)
    login = factory.Faker("user_name")
    type = factory.Faker("random_element", elements=["Organization", "User"])


class LicenseFactory(factory.DictFactory):
    key = factory.Faker("random_element", elements=list(LICENSES_METADATA.keys()))
    name = factory.LazyAttribute(lambda o: LICENSES_METADATA.get(o.key)["name"])
    spdx_id = factory.LazyAttribute(lambda o: LICENSES_METADATA.get(o.key)["spdx_id"])


class RepositorySummaryFactory(factory.DictFactory):
    id = fuzzy.FuzzyText(chars=string.digits, length=4)
    license = factory.SubFactory(LicenseFactory)
    owner = factory.SubFactory(OwnerFactory)
    name = factory.Faker("pystr")
    full_name = factory.LazyAttribute(lambda o: f"{o.owner['login']}/{o.name}")
    private = factory.Faker("random_element", elements=[True, False])
    html_url = factory.LazyAttribute(lambda o: f"https://github.com/{o.owner['login']}/{o.name}")
    description = factory.Faker("sentence", nb_words=4, variable_nb_words=False)
    stargazers_count = factory.Faker("pyint", min_value=0, max_value=100000)
    language = factory.Faker("random_element", elements=PROGRAMMING_LANGUAGES)


class RepositoriesFactory(factory.DictFactory):
    total_count = factory.Faker("pyint", min_value=0, max_value=10000000)
    incomplete_results = True
    pagination = {
        "prev": None,
        "next": None
    }

    @factory.post_generation
    def items(obj, create, extracted, **kwargs):
        if not create:
            return

        count = extracted or random.randint(1, 10)
        obj["items"] = [RepositorySummaryFactory() for _ in range(count)]
