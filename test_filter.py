import allure
import pytest

from pages.pages import Pages
from utilities.tests_queue import get_order


@allure.story("Взаимодействие с Фильтрами")
@allure.title("Поиск C2C смартфона с доп фильтрами, позитивный кейс")
@allure.testcase("https://app.qase.io/case/MKT-317")
@pytest.mark.order(get_order('test_main_filter_alpha'))
def test_main_filter_alpha(driver, home, pages, env):
    filter_page = pages.filter_page
    env = env
    match env:
        case "stage":
            constants = pages.constants.MarketStage
        case "prod":
            constants = pages.constants.MarketProd
        case "test":
            constants = pages.constants.MarketTest
        case "dev":
            constants = pages.constants.MarketTest
        case _:
            raise ValueError(f"Неизвестное окружение: {env}")

    pages.market_main_page.open_filter_page()
    filter_page.set_ads_type(constants.C2C)
    filter_page.set_location(constants.LOCATION_BISHKEK)
    filter_page.set_category(constants.CATEGORY_ELECTRONICS)
    filter_page.set_subcategory(constants.SUBCATEGORY_SMARTPHONE)
    filter_page.set_extra_data(constants.GADGET_MOBILE_KEY, constants.GADGET_MOBILE_VALUE)
    filter_page.set_extra_data(constants.CONDITION_KEY, constants.CONDITION_VALUE_NEW)
    filter_page.set_extra_data(constants.BRAND_MOBILE_KEY, constants.BRAND_MOBILE_VALUE_IPHONE)
    filter_page.open_extra_data()
    filter_page.set_extra_data(constants.RAM_KEY, constants.RAM_VALUE_2, constants.RAM_VALUE_4, constants.RAM_VALUE_6, constants.RAM_VALUE_8, constants.RAM_VALUE_16)
    filter_page.set_extra_data(constants.BATTERY_KEY, constants.BATTERY_VALUE_2000, constants.BATTERY_VALUE_2500, constants.BATTERY_VALUE_4000)
    filter_page.set_extra_data(constants.MATERIAL_KEY, constants.MATERIAL_VALUE_GLASS)
    filter_page.set_deal_type(constants.DEAL_TYPE_SELL)
    filter_page.set_price_range(constants.MIN_PRICE, constants.MAX_PRICE)
    filter_page.set_sort(constants.SORT_NEW)
    filter_page.show_ads()
    assert filter_page.is_ad_presents(constants.SEARCH_AD_IPHONE, with_scroll=True, attempts=10)


@allure.story("Взаимодействие с Фильтрами")
@allure.title("Поиск C2C смартфона по названию, позитивный кейс")
@allure.testcase("https://app.qase.io/case/MKT-317")
@pytest.mark.order(get_order('test_main_filter_betta'))
def test_main_filter_betta(driver, home, pages, env):
    omarket_page = pages.market_main_page
    filter_page = pages.filter_page
    env = env
    match env:
        case "stage":
            constants = pages.constants.MarketStage
        case "prod":
            constants = pages.constants.MarketProd
        case "test":
            constants = pages.constants.MarketTest
        case "dev":
            constants = pages.constants.MarketTest
        case _:
            raise ValueError(f"Неизвестное окружение: {env}")

    omarket_page.open_filter_page()
    filter_page.set_ads_type(constants.C2C)
    filter_page.set_word_to_search(constants.SEARCH_AD_IPHONE)
    driver.hide_keyboard()
    filter_page.show_ads()
    assert filter_page.is_ad_presents(constants.SEARCH_AD_IPHONE, with_scroll=True, attempts=10)
    filter_page.open_filter_page()
    filter_page.set_ads_type(constants.ALL)
    filter_page.set_word_to_search(constants.SEARCH_AD_AUTOTEST)
    driver.hide_keyboard()
    filter_page.show_ads()
    assert filter_page.is_ad_presents(constants.SEARCH_AD_IPHONE, with_scroll=True, attempts=10)
    filter_page.open_filter_page()
    filter_page.set_ads_type(constants.B2C)
    filter_page.set_word_to_search(constants.SEARCH_AD_IPHONE)
    driver.hide_keyboard()
    filter_page.show_ads()
    assert not filter_page.is_ad_presents(constants.SEARCH_AD_IPHONE, with_scroll=True, attempts=5)
