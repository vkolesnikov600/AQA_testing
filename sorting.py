
import time

import allure
import pytest

from tests.helpers.product_assertions import assert_prices_sorting


@pytest.fixture(autouse=True)
def ensure_webview_context(appium_client):
    appium_client.to_web_context()
    yield
    appium_client.to_native_context()


def assert_prices_in_range(prices, min_price: int, max_price: int, expected_count: int = 15):
    out_of_range_prices = [
        price for price in prices
        if not min_price <= price <= max_price
    ]

    assert len(prices) >= expected_count, (
        f"После изменения фильтра найдено только {len(prices)} товаров вместо {expected_count}. "
        f"Цены: {prices}"
    )
    assert not out_of_range_prices, (
        f"На первых {len(prices)} товарах найдены цены вне диапазона "
        f"{min_price} - {max_price}: {out_of_range_prices}. Все цены: {prices}"
    )


@allure.story("Сортировка")
@allure.feature("Сортировка товаров")
@allure.title("Применение нескольких фильтров перед сортировкой")
@allure.description(
    "Выбираем подкатегорию второго уровня Смартфоны, устанавливаем диапазон цены 10-100000, "
    "проверяем сортировку по цене и сохранение фильтров после изменения цены."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_sorting_with_multiple_filters(pages, appium_client):
    category_name = pages.constants.market.CATEGORY_ELECTRONICS
    subcategory_name = pages.constants.market.SUBCATEGORY_SMARTPHONE
    min_price = 10
    max_price = 100000
    updated_max_price = 50000
    expected_products_count = 15

    allure.dynamic.parameter("Категория", category_name)
    allure.dynamic.parameter("Подкатегория второго уровня", subcategory_name)
    allure.dynamic.parameter("Минимальная цена", min_price)
    allure.dynamic.parameter("Максимальная цена", max_price)
    allure.dynamic.parameter("Измененная максимальная цена", updated_max_price)

    with allure.step("Открываем категорию Электроника"):
        pages.filter_page.close_modal_if_open()
        pages.catalog_page.open_category_by_name(category_name, subcategory_name)
        assert pages.catalog_page.category_or_subcategory_is_opened(category_name, subcategory_name), (
            "Не открылась категория Электроника или подкатегория Смартфоны"
        )

    with allure.step("Выбираем подкатегорию Смартфоны и устанавливаем диапазон цены 10 - 100000"):
        pages.filter_page.open_modal()
        pages.filter_page.reset_filters_if_present()
        pages.filter_page.choose_subcategory_and_return_to_filter(subcategory_name)
        pages.filter_page.set_price_range(min_price, max_price)
        pages.filter_page.show_button_el().click()
        time.sleep(3)

        actual_subcategory_name = pages.catalog_page.subcategory_title_el().text.strip()
        assert subcategory_name in actual_subcategory_name, (
            f"Ожидалась подкатегория '{subcategory_name}', отображается '{actual_subcategory_name}'"
        )

    with allure.step("Дожидаемся обновления списка товаров"):
        products_count_element = appium_client.is_element_present(
            "xpath",
            '//p[@class="page-heading__subtitle"]',
            timeout=5,
        )
        product_cards = pages.catalog_page.all_product_els()
        empty_result = appium_client.is_element_present(
            "xpath",
            '//*[normalize-space(.)="Товары не найдены"]',
            timeout=2,
        )

        assert products_count_element or product_cards or empty_result, (
            "После применения нескольких фильтров список товаров не обновился"
        )

    with allure.step('Выбираем сортировку "Сначала дешёвые"'):
        pages.filter_page.choose_sorting("Сначала дешёвые")

    with allure.step('Проверяем сортировку "Сначала дешёвые" по возрастанию цены'):
        cheap_first_prices = pages.catalog_page.visible_product_prices(
            pages.utils,
            limit=expected_products_count,
        )
        assert_prices_sorting(
            cheap_first_prices,
            "Сначала дешёвые",
            descending=False,
            expected_count=expected_products_count,
        )

    with allure.step('Выбираем сортировку "Сначала дорогие"'):
        pages.filter_page.choose_sorting("Сначала дорогие")

    with allure.step('Проверяем сортировку "Сначала дорогие" по убыванию цены'):
        expensive_first_prices = pages.catalog_page.visible_product_prices(
            pages.utils,
            limit=expected_products_count,
        )
        assert_prices_sorting(
            expensive_first_prices,
            "Сначала дорогие",
            descending=True,
            expected_count=expected_products_count,
        )

    with allure.step("Изменяем ранее выбранный фильтр цены"):
        pages.filter_page.open_modal()
        pages.filter_page.set_price_range(min_price, updated_max_price)
        selected_filters_text = pages.filter_page.selected_filters_text()
        pages.filter_page.show_button_el().click()
        time.sleep(3)

    with allure.step("Проверяем, что остальные выбранные фильтры не сбросились"):
        normalized_selected_filters_text = selected_filters_text.lower().replace(" ", "")
        first_prices_after_price_change = pages.catalog_page.visible_product_prices(
            pages.utils,
            limit=expected_products_count,
        )

        assert subcategory_name.lower().replace(" ", "") in normalized_selected_filters_text, (
            f"После изменения цены фильтр подкатегории '{subcategory_name}' не найден "
            f"в выбранных фильтрах. Выбранные фильтры: {selected_filters_text}"
        )
        assert_prices_in_range(
            first_prices_after_price_change,
            min_price,
            updated_max_price,
            expected_count=expected_products_count,
        )
