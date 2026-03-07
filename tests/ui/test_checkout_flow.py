"""
tests/ui/test_checkout_flow.py

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
