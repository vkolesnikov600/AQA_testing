import time

import allure

from tests.helpers.product_assertions import assert_prices_sorting


@allure.story("Фильтры")
@allure.feature("Страница фильтрации")
@allure.title("Проверка отображения базовых фильтров")
@allure.description(
    "Нажимаем кнопку Фильтры и проверяем наличие базовых фильтров: Категория, Сортировка, "
    "Только в рассрочку, Только со скидкой, Цена от/до, Продавцы."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_base_filters_are_displayed(pages):
    category_name = pages.constants.market.CATEGORY_ELECTRONICS
    expected_filters = {
        "Категория": ["Категория"],
        "Сортировка": ["Сортировка"],
        "Только в рассрочку": ["Только в рассрочку", "рассрочку", "кредит"],
        "Только со скидкой": ["Только со скидкой", "со скидкой", "скидк"],
        "Цена": ["Цена"],
        "Продавцы": ["Продавцы"],
    }
    min_price = 1000
    max_price = 100000

    with allure.step("Открываем категорию Электроника"):
        pages.filter_page.close_modal_if_open()
        pages.catalog_page.open_category_by_name(category_name)
        actual_category_name = pages.catalog_page.subcategory_title_el().text.strip()
        assert category_name in actual_category_name, "Не открылась категория Электроника"

    with allure.step('Нажимаем кнопку "Фильтры"'):
        pages.filter_page.open_modal()
        assert pages.filter_page.filter_title_el().is_displayed(), "Страница фильтрации не открылась"

    with allure.step("Проверяем наличие базовых фильтров на странице фильтрации"):
        for filter_name, filter_aliases in expected_filters.items():
            assert pages.filter_page.filter_text_present(*filter_aliases), (
                f"Фильтр '{filter_name}' не отображается на странице фильтрации"
            )

        assert pages.filter_page.price_min_field_el().is_displayed(), "Поле цены 'от' не отображается"
        assert pages.filter_page.price_max_field_el().is_displayed(), "Поле цены 'до' не отображается"

    with allure.step('Включаем фильтр "Только в рассрочку"'):
        pages.filter_page.enable_toggle(pages.filter_page.on_credit_products_toggle_el())

    with allure.step("Применяем фильтрацию"):
        pages.filter_page.show_button_el().click()
        time.sleep(3)

    with allure.step("Проверяем отображаемые товары с кредитом/рассрочкой"):
        product_texts = pages.catalog_page.visible_product_card_texts()
        assert product_texts, "После применения фильтра 'Только в рассрочку' товары не отображаются"

        products_without_credit = [
            text for text in product_texts
            if (
                "рассроч" not in text.lower()
                and "кредит" not in text.lower()
                and "x6" not in text.lower()
                and "мес" not in text.lower()
            )
        ]
        assert not products_without_credit, (
            "Найдены товары без признака кредита/рассрочки: "
            f"{products_without_credit}"
        )

    with allure.step('Включаем фильтр "Только со скидкой"'):
        pages.filter_page.open_modal()
        pages.filter_page.enable_toggle(pages.filter_page.discounted_products_toggle_el())

    with allure.step("Применяем фильтрацию со скидкой"):
        pages.filter_page.show_button_el().click()
        time.sleep(3)

    with allure.step("Проверяем отображаемые товары со скидкой"):
        product_texts = pages.catalog_page.visible_product_card_texts()
        assert product_texts, "После применения фильтра 'Только со скидкой' товары не отображаются"
        assert pages.catalog_page.visible_old_price_present(), (
            "На странице нет товаров со скидкой после включения фильтра"
        )

    with allure.step("Указываем диапазон цены"):
        pages.filter_page.open_modal()
        pages.filter_page.reset_filters_if_present()
        pages.filter_page.set_price_range(min_price, max_price)

    with allure.step("Выбираем фильтр Продавцы и ищем Ostore"):
        pages.filter_page.sellers_el().click()
        pages.filter_page.choose_seller_by_search("Ostore")

    with allure.step("Нажимаем применить и Показать N товаров"):
        pages.filter_page.apply_button_el().click()
        pages.filter_page.show_button_el().click()
        time.sleep(3)

    with allure.step("Проверяем отображаемые товары по цене и продавцу"):
        product_texts = pages.catalog_page.visible_product_card_texts()
        assert product_texts, "После применения цены и продавца товары не отображаются"

        prices = [
            pages.utils.only_numbers(text)
            for text in pages.catalog_page.visible_product_price_texts()
        ]
        out_of_range_prices = [
            price for price in prices
            if not min_price <= price <= max_price
        ]
        assert not out_of_range_prices, (
            f"Найдены товары вне диапазона {min_price} - {max_price}: {out_of_range_prices}"
        )


@allure.story("Фильтры")
@allure.feature("Страница фильтрации")
@allure.title("Проверка сортировки на странице фильтрации")
@allure.description(
    "Выбираем сортировку по дешевым товарам, проверяем первые 15 цен по возрастанию, "
    "затем выбираем сортировку по дорогим товарам и проверяем первые 15 цен по убыванию."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_filter_modal_sorting_by_price(pages):
    category_name = pages.constants.market.CATEGORY_ELECTRONICS
    expected_products_count = 15

    with allure.step("Открываем категорию Электроника"):
        pages.filter_page.close_modal_if_open()
        pages.catalog_page.open_category_by_name(category_name)
        actual_category_name = pages.catalog_page.subcategory_title_el().text.strip()
        assert category_name in actual_category_name, "Не открылась категория Электроника"

    with allure.step('Выбираем сортировку "Сначала дешёвые"'):
        pages.filter_page.choose_sorting("Сначала дешёвые")

    with allure.step("Проверяем первые 15 товаров по возрастанию цены"):
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

    with allure.step("Проверяем первые 15 товаров по убыванию цены"):
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
