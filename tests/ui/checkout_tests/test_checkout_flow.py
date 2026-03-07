"""
tests/ui/checkout_tests/test_checkout_flow.py

End-to-end UI test for the SauceDemo checkout flow.

Test Steps:
  1. Log in with standard_user credentials
  2. Add Sauce Labs Backpack, Bolt T-Shirt, and Onesie to the cart;
     store the summed price
  3. Open the cart and remove the Bolt T-Shirt
  4. Proceed to checkout and fill in personal details
  5. On the overview page, assert:
     - Item subtotal equals the stored sum (minus removed item)
     - Tax is approximately 8% of item subtotal
     - Total = subtotal + tax
  6. Click Finish and assert the confirmation message
"""

from decimal import Decimal, ROUND_UP

import pytest
import pytest_check as check

from utils.constants import TestConstants
from utils.data_generator import generate_random_postal_code


def test_saucedemo_checkout_flow(setup_test):

    # Retrieve the initialized LoginPage from the fixture
    login_page = setup_test

    # 1. Login
    inventory_page = login_page.login("standard_user", "secret_sauce")

    # 2. Add products to cart and store sum of prices
    added_products = inventory_page.add_products_to_cart(TestConstants.PRODUCTS_TO_ADD)

    # Calculate initial sum
    initial_sum = sum(added_products.values())

    # 3. Navigate to Cart, Remove 'Sauce Labs Bolt T-Shirt', and proceed to checkout
    cart_page = inventory_page.go_to_cart()

    # Remove product from cart
    cart_page.remove_product(TestConstants.PRODUCT_TO_REMOVE)

    # Calculate the expected sum after removal
    price_of_removed_item = added_products[TestConstants.PRODUCT_TO_REMOVE.lower()]
    # expected_subtotal_after_removal = initial_sum - added_products[TestConstants.PRODUCT_TO_REMOVE]

    # Remove item from dict
    added_products.pop(TestConstants.PRODUCT_TO_REMOVE.lower())

    # Click checkout
    checkout_info_page = cart_page.click_checkout()

    # 4. Enter checkout information
    postal_code = generate_random_postal_code()
    checkout_info_page.fill_information(
        first_name="Test",
        last_name="User",
        postal_code=postal_code
    )

    # Click continue
    checkout_overview_page = checkout_info_page.click_continue()

    # 5. Perform Assertions on Checkout Overview
    actual_item_total = checkout_overview_page.get_item_total()
    actual_tax = checkout_overview_page.get_tax()
    actual_total = checkout_overview_page.get_total()

    expected_item_total = initial_sum - price_of_removed_item
    expected_tax = float(Decimal(expected_item_total * (TestConstants.TAX_PERCENTAGE / 100)).quantize(Decimal("0.00"), rounding=ROUND_UP))
    expected_total = float(Decimal(expected_item_total + expected_tax).quantize(Decimal("0.00"), rounding=ROUND_UP))

    # 5.1 Verify item total equals the stored sum (minus the removed item)
    check.equal(actual_item_total, expected_item_total,"Item total was not as expected")
    # 5.2 Verify tax is approximately 8% of Item total
    check.equal(actual_tax, expected_tax,"Tax was not as expected")
    # 5.3 Item total + Tax = Total
    check.equal(actual_total, expected_total, "Total was not as expected")

    checkout_complete_page = checkout_overview_page.click_finish()

    # 6. Final Verification
    actual_checkout_complete_successfully_msg = checkout_complete_page.get_confirmation_message()
    check.equal(actual_checkout_complete_successfully_msg, TestConstants.CHECKOUT_COMPLETE_SUCCESS_MSG,
                "Checkout complete message was not as expected")


@pytest.fixture(scope="function", autouse=True)
def setup_test(driver, config):
    # Navigate to SAUCE_DEMO_BASE_URL
    driver.get(config.BASE_UI_URL)

    # Instantiate the LoginPage and yield it to the test
    from pages.login_page import LoginPage
    login_page = LoginPage(driver)

    yield login_page
