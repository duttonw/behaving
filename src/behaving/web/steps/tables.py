from behave import then

from behaving.personas.persona import persona_vars
from splinter.exceptions import ElementDoesNotExist


def _process_table(table):

    headers = [el.text for el in table.find_by_tag("th")]
    # We should be using here rows = table.find_by_xpath("//tr[not(th)]")
    # but for some reason this duplicates the rows.
    rows = [r for r in table.find_by_tag("tr") if r.find_by_tag("td")]
    cells = [[cell.text for cell in row.find_by_tag("td")] for row in rows]
    return headers, cells


def _find_table_by_id_or_xpath(context, selector):
    try:
        table = context.browser.find_by_id(selector) or context.browser.find_by_xpath(
            selector
        )
        return table.first
    except (
        IndexError,
        ElementDoesNotExist,
    ):
        assert False, "Table not found"


@then('the table with id "{selector}" should be')
@then('the table with xpath "{selector}" should be')
@persona_vars
def table_equals(context, selector):
    table = _find_table_by_id_or_xpath(context, selector)
    headers, cells = _process_table(table)
    if headers:
        assert headers == context.table.headings, "Table headers do not match"

    assert [
        [cell for cell in row] for row in context.table.rows
    ] == cells, "Table cells do not match"


@then('the table with id "{selector}" should contain the rows')
@then('the table with xpath "{selector}" should contain the rows')
@persona_vars
def table_contains(context, selector):
    table = _find_table_by_id_or_xpath(context, selector)
    _, cells = _process_table(table)
    for row in [*context.table.rows, context.table.headings]:

        assert [cell for cell in row] in cells, f"{row} not found"


@then('the table with id "{selector}" should not contain the rows')
@then('the table with xpath "{selector}" should not contain the rows')
@persona_vars
def table_does_not_contain(context, selector):
    table = _find_table_by_id_or_xpath(context, selector)
    _, cells = _process_table(table)
    for row in [*context.table.rows, context.table.headings]:

        assert [cell for cell in row] not in cells, f"{row} found"


@then('row {row_no:d} in the table with id "{selector}" should be')
@then('row {row_no:d} in the table with xpath "{selector}" should be')
@persona_vars
def row_equals(context, row_no, selector):
    table = _find_table_by_id_or_xpath(context, selector)

    _, cells = _process_table(table)
    assert [cell for cell in context.table.headings] == cells[row_no]