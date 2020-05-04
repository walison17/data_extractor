import pytest
from openpyxl import Workbook

from data_extractor.exceptions import ExprError, ExtractError
from data_extractor.excel import ExcelExtractor


@pytest.fixture(scope="module")
def workbook():
    wb = Workbook()
    sheet = wb.create_sheet(title="users")

    sheet["A1"] = "username"
    sheet["B1"] = "country"

    sheet["A2"] = "walison17"
    sheet["B2"] = "brazil"

    sheet["A3"] = "linw1995"
    sheet["B3"] = "china"

    return wb


@pytest.fixture(scope="module")
def element(workbook):
    return workbook["users"]


@pytest.mark.parametrize(
    "expr,expect",
    [
        ("A1", ["username"]),
        ("A2", ["walison17"]),
    ],
    ids=repr,
)
def test_extract(element, expr, expect):
    extractor = ExcelExtractor(expr)
    assert expect == extractor.extract(element)


@pytest.mark.usefixtures("json_extractor_backend")
@pytest.mark.parametrize(
    "expr,expect",
    [
        ("A1", "username"),
        ("A9", "default"),
        ("A2", "walison17"),
        ("B2", "brazil"),
        ("B9", "default"),
    ],
    ids=repr,
)
def test_extract_first(element, expr, expect):
    extractor = ExcelExtractor(expr)
    assert expect == extractor.extract_first(element, default="default")


@pytest.mark.parametrize("expr", ["A9", "B9"], ids=repr)
def test_extract_first_without_default(element, expr):
    extractor = ExcelExtractor(expr)

    with pytest.raises(ExtractError) as catch:
        extractor.extract_first(element)

    exc = catch.value
    assert len(exc.extractors) == 1
    assert exc.extractors[0] is extractor
    assert exc.element is element


@pytest.mark.parametrize("expr", ["Aaaa", "Bbbb"])
def test_invalid_cell_coordinate(element, expr):
    extractor = ExcelExtractor(expr)

    with pytest.raises(ExprError) as catch:
        extractor.extract(element)

    exc = catch.value
    assert exc.extractor is extractor


@pytest.mark.parametrize(
    "expr,expect",
    [
        ("A2:B2", ["walison17", "brazil"]),
        ("A3:B3", ["linw1995", "china"]),
        ("A2:D3", ["walison17", "brazil", "linw1995", "china"]),
    ],
    ids=repr,
)
def test_extract_cell_range(element, expr, expect):
    extractor = ExcelExtractor(expr)
    assert extractor.extract(element) == expect
