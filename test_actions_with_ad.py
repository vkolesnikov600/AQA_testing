import time
import allure
import pytest

from utilities.tests_queue import get_order


@allure.story("Взаимодействие с карточкой товара")
@allure.title("Добавить и удалить товар с избранного (п.1-3)")
@allure.testcase("https://app.qase.io/case/MKT-320")
@pytest.mark.order(get_order('test_add_delete_from_favorite'))
def test_add_delete_from_favorite(driver, env, home, pages):
    omarket_main_page = pages.market_main_page
    ad_view_page = pages.ad_view_page
    profile_page = pages.profile_page
    favorite_page = pages.favorites_page
    env = env

    omarket_main_page.is_switcher_active("B2C")
    omarket_main_page.click_first_ad_card(check_18=True)
    ad_view_page.click_add_to_favorite()
    ad_title = ad_view_page.get_ad_title()
    omarket_main_page.click_go_to_profile()
    profile_page.click_go_to_subsection(profile_page.locators.FAVORITES)
    assert favorite_page.is_ad_exists(ad_title)
    favorite_page.click_to_ad_card(ad_title)
    ad_view_page.click_remove_from_favorite()


@allure.story("Взаимодействие с карточкой товара")
@allure.title("Взаимодействие с доставкой товара (п.5)")
@allure.testcase("https://app.qase.io/case/MKT-320")
@pytest.mark.order(get_order('test_delivery_pickup'))
def test_delivery_pickup(driver, home, pages):
    omarket_main_page = pages.market_main_page
    ad_view_page = pages.ad_view_page
    delivery_terms_page = pages.delivery_terms_page
    payment_page = pages.payment_page

    omarket_main_page.click_first_ad_card(check_18=True)
    ad_view_page.click_search_handle_error(ad_view_page.locators.DELIVERY_TERMS)
    time.sleep(3)
    delivery_terms_page.click_delivery_button()
    assert delivery_terms_page.check_is_map_presents()
    delivery_terms_page.click_create_order_button()
    assert payment_page.check_is_delivery_active()
    payment_page.click_back_button()
    assert delivery_terms_page.check_is_delivery_active()
    assert delivery_terms_page.check_is_delivery_info_presents()
    delivery_terms_page.click_pickup_button()
    assert delivery_terms_page.check_is_pickup_info_presents
    delivery_terms_page.click_create_order_button()
    assert payment_page.check_is_pickup_active()
    payment_page.click_back_button()
    assert delivery_terms_page.check_is_pickup_active()
    delivery_terms_page.click_back_button()
    assert ad_view_page.check_is_ad_page()



# @allure.story("Взаимодействие с карточкой товара")
# @allure.title("Взаимодействие с жалобами на товар (п.6-9)")
# @allure.testcase("https://app.qase.io/case/MKT-320")
# @pytest.mark.order(get_order('test_complaint_to_ad'))
# def test_complaint_to_ad(driver, market_home):
#     omarket = MainPage(driver)
#     ad_view = AdViewPage(driver)
#
#     omarket.click_first_ad_card()
#     ad_view.click_three_dots()
#     ad_view.click_complaint()
    #Добавить проверку, что комментарий более 20 символов (разблокировка кнопки Отправить)


@allure.story("Взаимодействие с объявлением")
@allure.title("Создание объявления")
@allure.testcase("https://app.qase.io/case/MKT-321")
@pytest.mark.order(get_order('test_create_ad'))
def test_create_ad(driver, home, pages, env):
    omarket_page = pages.market_main_page
    create_ad_page = pages.create_ad_page
    profile_page = pages.profile_page
    ad_page = pages.ad_view_page
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

    omarket_page.click_switch_to_c2c()
    omarket_page.click_create_ad()
    ad_title = create_ad_page.set_ad_title()
    create_ad_page.set_ad_description()
    driver.hide_keyboard()
    # create_ad_page.upload_ad_photo(constants.PHOTO_IPHONE_PATH)
    create_ad_page.get_element(create_ad_page.locators.NEXT_BUTTON).click()

    time.sleep(3)
    create_ad_page.get_element(create_ad_page.locators.SEARCH).send_keys(constants.CATEGORY_ELECTRONICS)
    create_ad_page.get_element(create_ad_page.locators.CATEGORY_ELEMENT.format(constants.CATEGORY_ELECTRONICS)).click()
    create_ad_page.get_element(create_ad_page.locators.CATEGORY_ELEMENT.format(constants.SUBCATEGORY_SMARTPHONE)).click()
    # create_ad_page.get_element(create_ad_page.locators.NEXT_BUTTON).click()

    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_BUTTON.format(constants.DEAL_TYPE_KEY)).click()
    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_VALUE_CONTAINS.format(constants.DEAL_TYPE_SELL)).click()
    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_BUTTON.format(constants.GADGET_MOBILE_KEY)).click()
    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_VALUE.format(constants.GADGET_MOBILE_VALUE)).click()
    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_BUTTON.format(constants.BRAND_MOBILE_KEY)).click()
    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_VALUE.format(constants.BRAND_MOBILE_VALUE_SAMSUNG)).click()
    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_BUTTON.format(constants.CONDITION_KEY)).click()
    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_VALUE.format(constants.CONDITION_VALUE_NEW)).click()
    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_BUTTON.format(constants.WORK_SCHEDULE_KEY)).click()
    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_VALUE.format(constants.WORK_SCHEDULE_VALUE)).click()
    create_ad_page.click_search_handle_error(create_ad_page.locators.DETAIL_INPUT_BUTTON.format(constants.RAM_KEY))
    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_VALUE.format(constants.RAM_VALUE_4)).click()
    create_ad_page.click_search_handle_error(create_ad_page.locators.DETAIL_INPUT_BUTTON.format(constants.EQUIPMENT_KEY))
    create_ad_page.get_element(create_ad_page.locators.DETAIL_MULTI_INPUT_VALUE.format(constants.EQUIPMENT_VALUE_GLASS)).click()
    create_ad_page.get_element(create_ad_page.locators.DETAIL_MULTI_INPUT_VALUE.format(constants.EQUIPMENT_VALUE_CHARGER)).click()
    create_ad_page.get_element(create_ad_page.locators.DETAIL_MULTI_INPUT_VALUE.format(constants.EQUIPMENT_VALUE_CABLE)).click()
    create_ad_page.get_element(create_ad_page.locators.READY_BUTTON).click()
    create_ad_page.click_search_handle_error(create_ad_page.locators.DETAIL_INPUT_BUTTON.format(constants.SIM_KEY))
    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_VALUE.format(constants.SIM_VALUE_2)).click()
    create_ad_page.get_element(create_ad_page.locators.NEXT_BUTTON).click()

    create_ad_page.get_element(create_ad_page.locators.PRICE_INPUT).send_keys(constants.AD_PRICE_150k)
    driver.hide_keyboard()
    create_ad_page.get_element(create_ad_page.locators.NEXT_BUTTON).click()

    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_BUTTON.format(constants.LOCATION_KEY)).click()
    create_ad_page.get_element(create_ad_page.locators.DETAIL_INPUT_VALUE.format(constants.LOCATION_BISHKEK)).click()
    create_ad_page.get_element(create_ad_page.locators.TELEGRAM_CHECKBOX).click()
    create_ad_page.get_element(create_ad_page.locators.TELEGRAM_INPUT).send_keys(constants.TELEGRAM_LOGIN)
    driver.hide_keyboard()
    create_ad_page.get_element(create_ad_page.locators.NEXT_BUTTON).click()

    create_ad_page.get_element(create_ad_page.locators.PUBLISH_BUTTON).click()
    create_ad_page.get_element(create_ad_page.locators.SKIP_PROMOTION).click()
    assert ad_page.get_ad_title() == ad_title


# @allure.story("Взаимодействие с БД")
# @allure.title("Тестовый запрос в БД")
# def test_insert_select_to_db(driver, market_home):
#     omarket = MainPage(driver)
#
#     omarket.select_user_data('996509583420')
#     omarket.insert_user_data('996509583420')


@allure.story("Взаимодействие с объявлением")
@allure.title("Редактирование и удаление объявления")
@allure.testcase("https://app.qase.io/case/MKT-321")
@pytest.mark.order(get_order('test_edit_delete_ad'))
def test_edit_delete_ad(driver, home, pages, env):
    omarket_page = pages.market_main_page
    profile_page = pages.profile_page
    ad_own_view_page = pages.ad_own_view_page
    ad_edit_page = pages.ad_edit_page
    ad_view_page = pages.ad_view_page
    create_ad_page = pages.create_ad_page
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

    omarket_page.click_go_to_profile()
    flag = profile_page.is_first_ad_title_equals(constants.EDIT_TITLE)
    profile_page.click_to_first_ad()
    ad_own_view_page.edit_ad()

    ad_edit_page.edit_title(constants.EDIT_TITLE)
    driver.hide_keyboard()
    create_ad_page.get_element(create_ad_page.locators.NEXT_BUTTON).click()
    create_ad_page.click_search_handle_error(create_ad_page.locators.CHECKED_CATEGORY)
    create_ad_page.click_search_handle_error(create_ad_page.locators.CHECKED_CATEGORY)
    create_ad_page.get_element(create_ad_page.locators.NEXT_BUTTON).click()
    create_ad_page.get_element(create_ad_page.locators.NEXT_BUTTON).click()
    create_ad_page.get_element(create_ad_page.locators.NEXT_BUTTON).click()
    create_ad_page.get_element(create_ad_page.locators.PUBLISH_BUTTON).click()
    create_ad_page.get_element(create_ad_page.locators.SKIP_PROMOTION).click()
    assert ad_view_page.is_ad_edited(constants.EDIT_TITLE, flag)

    ad_title = ad_view_page.get_ad_title()
    ad_view_page.click_search_handle_error(ad_view_page.locators.THREE_DOTS)
    ad_view_page.get_element(ad_view_page.locators.DELETE_AD).click()
    ad_view_page.get_element(ad_view_page.locators.DELETE_AD_CONFIRM).click()
    ad_view_page.get_element(ad_view_page.locators.IS_DEAL_SUCCESS_CHECKBOX).click()
    ad_view_page.get_element(ad_view_page.locators.SEND_ANSWER).click()
    time.sleep(8)
    assert profile_page.is_first_ad_id_not_equals(ad_title)
