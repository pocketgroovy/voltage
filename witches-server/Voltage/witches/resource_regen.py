def get_sanitized_stamina(requested_stamina, requested_stamina_potions, user, max_stamina):
    num_stamina = user.ticket
    num_potions = user.stamina_potion

    # Prevent more than max stamina
    if requested_stamina > max_stamina:
        excess_stamina = requested_stamina - max_stamina
        requested_stamina = max_stamina
        requested_stamina_potions += excess_stamina
    
    # Calculate difference in stamina
    needed_stamina = requested_stamina - user.ticket
    if needed_stamina > 0:
        if needed_stamina <= num_potions:
            num_stamina += needed_stamina
            num_potions -= needed_stamina
        else:
            # User doesn't have enough potions to cover the cost
            num_stamina += num_potions
            num_potions = 0
    else:
        # Requested value is fine
        num_stamina = requested_stamina

    # Take whichever stamina potion value is lower
    num_potions = min(num_potions, requested_stamina_potions)

    # Ensure the resulting values are not negative
    if num_stamina < 0:
        num_stamina = 0

    if num_potions < 0:
        num_potions = 0

    return num_stamina, num_potions

