import os

from behaving import environment as benv


def before_all(context):
    import behaving

    context.remote_webdriver_url = "http://selenoid:4444/wd/hub"
    context.default_browser = "chrome"
    context.accept_ssl_certs = True
    # https://aerokube.com/selenoid/latest/
    context.browser_args = {
        "desired_capabilities": {
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": False
            },
        }
    }
    context.attachment_dir = os.path.join(
        os.path.dirname(behaving.__file__), "../../tests/data"
    )
    context.sms_path = os.path.join(
        os.path.dirname(behaving.__file__), "../../var/sms/"
    )
    context.mail_path = os.path.join(
        os.path.dirname(behaving.__file__), "../../var/mail/"
    )
    context.gcm_path = os.path.join(
        os.path.dirname(behaving.__file__), "../../var/gcm/"
    )
    context.screenshots_dir = os.path.join(
        os.path.dirname(behaving.__file__), "../../var/screenshots/"
    )
    context.download_dir = os.path.join(
        os.path.dirname(behaving.__file__), "../../var/downloads/"
    )
    benv.before_all(context)


def after_all(context):
    benv.after_all(context)


def before_feature(context, feature):
    benv.before_feature(context, feature)
    if "no_remote_webdriver" in feature.tags and context.remote_webdriver_url:
        feature.skip("Skipped feature, running in remote webdriver @skip")


def after_feature(context, feature):
    benv.after_feature(context, feature)


def before_scenario(context, scenario):
    benv.before_scenario(context, scenario)
    if "no_remote_webdriver" in scenario.tags and context.remote_webdriver_url:
        scenario.skip("Skipped feature, running in remote webdriver @skip")


def after_scenario(context, scenario):
    benv.after_scenario(context, scenario)
