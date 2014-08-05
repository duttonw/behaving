import time
from behave import step

from selenium.common.exceptions import NoSuchElementException

from behaving.personas.persona import persona_vars

# Accepts a lambda as second paramter, returns lambda result on success, or False on timeout
def retry(timeout, func, delay=1):
    start = time.time()
    while True:
        try:
            res = func()
            if res is False or res is None:
                time.sleep(delay)
            else:
                return res
        except:
            time.sleep(delay)

        if time.time() - start > timeout:
            return False


def raise_element_not_found_exception(name, context):
    def list_elements_from_context(context):
        elements = context.device.find_elements_by_ios_uiautomation('.elements()')
        return [el.get_attribute("name") for el in elements]

    assert False, u'Element "%s" not found. Available elements: %s' % (name, list_elements_from_context(context))


def texts_on_device(context):
    elems = context.device.find_elements_by_ios_uiautomation('.elements()')
    return [e.text for e in elems]


def text_exists_on_device(context, text):
    # This should be replaced with something more sane
    # It also only works on iOS
    for t in texts_on_device(context):
        try:
            if text in str(t):
                return True
        except UnicodeEncodeError:
            pass

    return False


@step(u'I wait for {timeout:d} seconds')
@persona_vars
def wait_for_timeout(context, timeout):
    time.sleep(timeout)


@step(u'I show the element with id "{id}"')
@persona_vars
def show_element_by_id(context, id):
    assert context.browser.find_by_id(id)
    context.browser.execute_script('document.getElementById("%s").style.display="inline";' % id)


@step(u'I hide the element with id "{id}"')
@persona_vars
def hide_element_by_id(context, id):
    assert context.browser.find_by_id(id)
    context.browser.execute_script('document.getElementById("%s").style.display="none";' % id)


@step(u'I should see "{text}"')
@persona_vars
def should_see(context, text):
    if hasattr(context, 'browser'):
        assert context.browser.is_text_present(text), u'Text not found'
    elif hasattr(context, 'device'):
        if not text_exists_on_device(context, text):
            assert False, u'Text not found. Available text: "%s"' % '", "'.join(texts_on_device(context))


@step(u'I should not see "{text}"')
@persona_vars
def should_not_see(context, text):
    if hasattr(context, 'browser'):
        assert context.browser.is_text_not_present(text), u'Text was found'
    elif hasattr(context, 'device'):
        if text_exists_on_device(context, text):
            assert False, u'Text found'


@step(u'I should see "{text}" within {timeout:d} seconds')
@persona_vars
def should_see_within_timeout(context, text, timeout):
    if hasattr(context, 'browser'):
        assert context.browser.is_text_present(text, wait_time=timeout), u'Text not found'
    elif hasattr(context, 'device'):
        assert retry(timeout, lambda: text_exists_on_device(context, text)), u'Text not found'


@step(u'I should not see "{text}" within {timeout:d} seconds')
@persona_vars
def should_not_see_within_timeout(context, text, timeout):
    if hasattr(context, 'browser'):
        assert context.browser.is_text_not_present(text, wait_time=timeout), u'Text was found'
    elif hasattr(context, 'device'):
        assert retry(timeout, lambda: not text_exists_on_device(context, text)), u'Text was found'


@step(u'I should see an element with id "{id}"')
@persona_vars
def should_see_element_with_id(context, id):
    if hasattr(context, 'browser'):
        assert context.browser.is_element_present_by_id(id), u'Element not present'
    elif hasattr(context, 'device'):
        try:
            context.device.find_element_by_name(id)
        except NoSuchElementException:
            raise_element_not_found_exception(id, context)


@step(u'I should not see an element with id "{id}"')
@persona_vars
def should_not_see_element_with_id(context, id):
    if hasattr(context, 'browser'):
        assert context.browser.is_element_not_present_by_id(id), u'Element is present'
    elif hasattr(context, 'device'):
        try:
            context.device.find_element_by_name(id)
            assert False, u'Element is present'
        except NoSuchElementException:
            pass


@step(u'I should see an element with id "{id}" within {timeout:d} seconds')
@persona_vars
def should_see_element_with_id_within_timeout(context, id, timeout):
    if hasattr(context, 'browser'):
        assert context.browser.is_element_present_by_id(id, wait_time=timeout), u'Element not present'
    elif hasattr(context, 'device'):
        if not retry(timeout, lambda: context.device.find_element_by_name(id)):
           raise_element_not_found_exception(id, context)

@step(u'I should not see an element with id "{id}" within {timeout:d} seconds')
@persona_vars
def should_not_see_element_with_id_within_timeout(context, id, timeout):
    if hasattr(context, 'browser'):
        assert context.browser.is_element_not_present_by_id(id, wait_time=timeout), u'Element is present'
    elif hasattr(context, 'device'):
        assert not retry(timeout, lambda: context.device.find_element_by_name(id)), u'Element is present'


@step(u'I should see an element with the css selector "{css}"')
def should_see_element_with_css(context, css):
    assert context.browser.is_element_present_by_css(css), u'Element not present'


@step(u'I should not see an element with the css selector "{css}"')
def should_not_see_element_with_css(context, css):
    assert context.browser.is_element_not_present_by_css(css), u'Element is present'


@step(u'I should see an element with the css selector "{css}" within {timeout:d} seconds')
def should_see_element_with_css_within_timeout(context, css, timeout):
    assert context.browser.is_element_present_by_css(css, wait_time=timeout), u'Element not present'


@step(u'I should not see an element with the css selector "{css}" within {timeout:d} seconds')
def should_not_see_element_with_css_within_timeout(context, css, timeout):
    assert context.browser.is_element_not_present_by_css(css, wait_time=timeout), u'Element is present'


@step(u'I should see an element with xpath "{xpath}"')
@persona_vars
def should_see_element_with_xpath(context, xpath):
    assert context.browser.is_element_present_by_xpath(xpath), u'Element not present'


@step(u'I should not see an element with xpath "{xpath}"')
@persona_vars
def should_not_see_element_with_xpath(context, xpath):
    assert context.browser.is_element_not_present_by_xpath(xpath), u'Element is present'


@step(u'I should see an element with xpath "{xpath}" within {timeout:d} seconds')
@persona_vars
def should_see_element_with_xpath_within_timeout(context, xpath, timeout):
    assert context.browser.is_element_present_by_xpath(xpath, wait_time=timeout), u'Element not present'


@step(u'I should not see an element with xpath "{xpath}" within {timeout:d} seconds')
@persona_vars
def should_not_see_element_with_xpath_within_timeout(context, xpath, timeout):
    assert context.browser.is_element_not_present_by_xpath(xpath, wait_time=timeout), u'Element is present'


@step(u'I execute the script "{script}"')
def execute_script(context, script):
    context.browser.execute_script(script)


@step(u'I evaluate the script "{script}" and assign the result to "{key}"')
def evaluate_script(context, script, key):
    assert context.persona is not None, u'no persona is setup'
    context.persona[key] = context.browser.evaluate_script(script)
