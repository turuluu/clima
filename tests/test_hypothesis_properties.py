"""Property-based tests using Hypothesis.

Targets pure helpers in clima.utils and clima.schema. These helpers have
no global state and no I/O, so they make natural fits for property testing.
"""
import keyword
from collections import namedtuple

from hypothesis import given, strategies as st

from clima.utils import chain_get, filter_fields
from clima.schema import should_wrap_as_list


# Python identifiers usable as namedtuple field names — must not be keywords.
_ident = st.from_regex(r"\A[a-z][a-z0-9_]{0,7}\Z").filter(
    lambda s: not keyword.iskeyword(s)
)


@st.composite
def _dict_and_schema(draw):
    field_names = draw(
        st.lists(_ident, min_size=0, max_size=6, unique=True)
    )
    NT = namedtuple("NT", field_names) if field_names else namedtuple("NT", [])
    extra_keys = draw(st.lists(_ident, min_size=0, max_size=6, unique=True))
    all_keys = list(set(field_names) | set(extra_keys))
    values = draw(
        st.lists(st.integers(), min_size=len(all_keys), max_size=len(all_keys))
    )
    d = dict(zip(all_keys, values))
    return d, NT


@given(_dict_and_schema())
def test_filter_fields_is_intersection(params):
    d, NT = params
    result = filter_fields(d, NT)
    assert set(result.keys()) == set(d.keys()) & set(NT._fields)
    for k, v in result.items():
        assert d[k] == v


@given(_dict_and_schema())
def test_filter_fields_is_idempotent(params):
    d, NT = params
    once = filter_fields(d, NT)
    twice = filter_fields(once, NT)
    assert once == twice


@given(st.lists(st.one_of(st.none(), st.integers(min_value=1)), min_size=1, max_size=8))
def test_chain_get_returns_first_non_none(values):
    first_non_none = next((v for v in values if v is not None), None)

    def make(v):
        return lambda: v

    calls = tuple((make(v),) for v in values)
    if first_non_none is None:
        # chain_get with fail=False returns None when all callables yield None.
        assert chain_get(*calls) is None
    else:
        assert chain_get(*calls) == first_non_none


@given(st.one_of(st.integers(), st.floats(allow_nan=False), st.text(min_size=0, max_size=10)))
def test_should_wrap_scalar_for_list_target(value):
    # Non-iterable scalars (and bare strings) should be wrapped when the
    # target type is list — MetaSchema relies on this to avoid splitting
    # a string into its characters via list(str).
    assert should_wrap_as_list(value, list) is True


@given(st.lists(st.integers(), min_size=0, max_size=5))
def test_should_not_wrap_list_when_target_is_list(value):
    # A list value targeting list should not be re-wrapped.
    assert should_wrap_as_list(value, list) is False
