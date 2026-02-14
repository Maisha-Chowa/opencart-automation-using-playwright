"""Page Object Model classes for OpenCart automation."""

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.search_page import SearchPage
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage

__all__ = [
    "HomePage",
    "ProductPage",
    "CartPage",
    "SearchPage",
    "RegisterPage",
    "LoginPage",
    "CheckoutPage",
]
