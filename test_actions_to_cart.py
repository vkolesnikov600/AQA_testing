import pytest

import allure
from sympy.solvers.diophantine.diophantine import base_solution_linear

from pages.pages import Pages
from utilities.tests_queue import get_order


@allure.story("Взаимодействие с главной страницей")
@allure.title("Добавить и Удалить товар из корзины на главной странице через карточку товара")
@allure.testcase("https://app.qase.io/case/MKT-317")
@pytest.mark.order(get_order('test_add_delete_to_cart'))
def test_add_delete_to_cart(driver, home, pages):
    # Инициализация страницы
    omarket_main_page = pages.market_main_page

    # Получить счетчик корзины, инициализировать счетчик товара и инициализировать счетчик товара на карточке
    basket_counter_before = omarket_main_page.get_basket_counter()
    ad_counter_before = 0
    # Добавить товар в корзину и получить счетчик корзины и товара
    omarket_main_page.click_add_to_basket(check_18=True)
    basket_counter_after = omarket_main_page.get_basket_counter()
    ad_counter_after = omarket_main_page.get_ad_counter()
    # Проверить что счетчик корзины, товара и карточки увеличился после добавления товара в корзину
    assert omarket_main_page.is_counter_incremented(basket_counter_before, basket_counter_after)
    assert omarket_main_page.is_counter_incremented(ad_counter_before, ad_counter_after)
    # Приравнять счетчики к последнему актуальному значению и увеличить кол-во товара в корзине на 1 единицу
    basket_counter_before = basket_counter_after
    ad_counter_before = ad_counter_after
    omarket_main_page.click_increment_ad_quantity(check_18=True)
    # Получить все счетчики и проверить что их количество увеличилось
    basket_counter_after = omarket_main_page.get_basket_counter()
    ad_counter_after = omarket_main_page.get_ad_counter()
    assert omarket_main_page.is_counter_incremented(basket_counter_before, basket_counter_after)
    assert omarket_main_page.is_counter_incremented(ad_counter_before, ad_counter_after)
    # Приравнять счетчики к последнему актуальному значению и уменьшить кол-во товара на 1 единицу
    basket_counter_before = basket_counter_after
    ad_counter_before = ad_counter_after
    omarket_main_page.click_decrement_ad_quantity(check_18=True)
    # Получить счетчики и проверить что их кол-во уменьшилось
    basket_counter_after = omarket_main_page.get_basket_counter()
    ad_counter_after = omarket_main_page.get_ad_counter()
    assert omarket_main_page.is_counter_decremented(basket_counter_before, basket_counter_after)
    assert omarket_main_page.is_counter_decremented(ad_counter_before, ad_counter_after)
    # Приравнять счетчики к последнему актуальному значению и удалить товар из корзины
    basket_counter_before = basket_counter_after
    ad_counter_before = ad_counter_after
    omarket_main_page.click_delete_from_basket(check_18=True)
    # Получить счетчики и проверить что их кол-во уменьшилось
    basket_counter_after = omarket_main_page.get_basket_counter()
    ad_counter_after = 0
    assert omarket_main_page.is_counter_decremented(basket_counter_before, basket_counter_after)
    assert omarket_main_page.is_counter_decremented(ad_counter_before, ad_counter_after)


@allure.story("Взаимодействие с главной страницей")
@allure.title("Добавить и Удалить товар из корзины через страницу товара")
@allure.testcase("https://app.qase.io/case/MKT-318")
@pytest.mark.order(get_order('test_add_delete_to_cart_from_ad'))
def test_add_delete_to_cart_from_ad(driver, home, pages):
    # Инициализация страницы
    omarket_main_page = pages.market_main_page
    ad_view_page = pages.ad_view_page
    basket_page = pages.basket_page

    omarket_main_page.go_to_basket()
    basket_page.delete_all_ads(check_18=True)
    # Перейти по карточке первого товара, получить счетчик корзины, получить название объявления и добавить товар в корзину
    omarket_main_page.click_first_ad_card(check_18=True)
    basket_counter_before = ad_view_page.get_basket_counter()
    ad_title = ad_view_page.get_ad_title()
    ad_view_page.click_add_to_basket(check_18=True)
    # Получить счетчик и проверить что он увеличился
    basket_counter_after = ad_view_page.get_basket_counter()
    assert ad_view_page.is_counter_incremented(basket_counter_before, basket_counter_after)
    # Проверить что товар на самом деле есть в корзине и очистить корзину
    ad_view_page.click_go_to_basket(check_18=True)
    assert basket_page.is_ad_exists(ad_title)
    basket_page.delete_all_ads()


@allure.story("Взаимодействие с главной страницей")
@allure.title("Добавление товара в корзину на странице продавца")
@allure.testcase("https://app.qase.io/case/MKT-319")
@pytest.mark.order(get_order('test_add_delete_to_cart_from_merchant'))
def test_add_delete_to_cart_from_merchant(driver, home, pages):
    # Инициализация страницы
    omarket = pages.market_main_page
    merchant_page = pages.merchant_page
    basket_page = pages.basket_page
    # Почистить корзину
    omarket.go_to_basket()
    basket_page.delete_all_ads(check_18=True)
    # Перейти по баннеру мерчанта, добавить первый товар в корзину и проверить что он добавился
    omarket.click_banner_merchant()
    ad_title = merchant_page.get_ad_title()
    merchant_page.click_add_to_basket(check_18=True)
    omarket.go_to_basket()
    assert basket_page.is_ad_exists(ad_title)
    basket_page.click_go_back()
    # Удалить товар из корзины и проверить что он удалился
    merchant_page.click_delete_from_basket()
    omarket.go_to_basket()
    assert basket_page.is_ad_exists(ad_title) is False
    basket_page.delete_all_ads()

