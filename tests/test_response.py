import pytest

from bitex.response import BitexResponse


def test_triple_method_raises_not_implemented_error():
    with pytest.raises(NotImplementedError):
        BitexResponse().triples()


def test_key_value_dict_raises_not_implemented_error():
    with pytest.raises(NotImplementedError):
        BitexResponse().key_value_dict()


def test_repr_magic_method_returns_correct_string():
    resp = BitexResponse()
    resp.status_code = 200
    assert repr(resp) == "<BitexResponse [200]>"
