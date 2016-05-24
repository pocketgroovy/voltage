from django.utils import unittest

from witches.resource_regen import get_sanitized_stamina
        
class User(object):
    def __init__(self, ticket=0, stamina_potion=0, focus=0):
        self.ticket = ticket
        self.stamina_potion = stamina_potion


class StaminaRegenTests(unittest.TestCase):
    def setUp(self):
        self.max_stamina = 5
        
    def test_with_no_change__shows_no_change(self):
        user = User(3, 1)

        (stamina, stamina_pots) = get_sanitized_stamina(3, 1, user, self.max_stamina)
        self.assertEqual(3, stamina)
        self.assertEqual(1, stamina_pots)

    def test_with_used_stamina__returns_used_stamina(self):
        user = User(5, 1)

        (stamina, stamina_pots) = get_sanitized_stamina(3, 1, user, self.max_stamina)
        self.assertEqual(3, stamina)
        self.assertEqual(1, stamina_pots)

    def test_when_invalid_potions__uses_server_potions(self):
        user = User(1, 2)
        (stamina, stamina_pots) = get_sanitized_stamina(1, 4, user, self.max_stamina)
        self.assertEqual(1, stamina)
        self.assertEqual(2, stamina_pots)

    def test_when_need_stamina__uses_potions(self):
        user = User(1, 4)
        (stamina, stamina_pots) = get_sanitized_stamina(4, 4, user, self.max_stamina)
        self.assertEqual(4, stamina)
        self.assertEqual(1, stamina_pots)

    def test_when_not_enough_stamina_and_potions__converts_all_potions_into_stamina(self):
        user = User(1, 2)
        (stamina, stamina_pots) = get_sanitized_stamina(4, 4, user, self.max_stamina)
        self.assertEqual(3, stamina)
        self.assertEqual(0, stamina_pots)

    def test_with_negative_stamina__stamina_becomes_0(self):
        user = User(1, 2)
        (stamina, stamina_pots) = get_sanitized_stamina(-1, 2, user, self.max_stamina)
        self.assertEqual(0, stamina)
        self.assertEqual(2, stamina_pots)

    def test_with_negative_potions__potions_becomes_0(self):
        user = User(1, 2)
        (stamina, stamina_pots) = get_sanitized_stamina(1, -2, user, self.max_stamina)
        self.assertEqual(1, stamina)
        self.assertEqual(0, stamina_pots)

    def test_with_more_than_max_stamina__stamina_is_set_to_max_and_potions_receive_the_difference(self):
        user = User(4, 3)
        (stamina, stamina_pots) = get_sanitized_stamina(6, 1, user, self.max_stamina)
        self.assertEqual(5, stamina)
        self.assertEqual(2, stamina_pots)

    def test_with_more_than_max_stamina_and_no_resources__values_are_distributed_correctly(self):
        user = User(4, 3)
        (stamina, stamina_pots) = get_sanitized_stamina(8, 1, user, self.max_stamina)
        self.assertEqual(5, stamina)
        self.assertEqual(2, stamina_pots)


