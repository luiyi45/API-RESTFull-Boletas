def point_of_sale_to_dict(pos):

    return {
        "id": pos.id,
        "name": pos.name,
        "address": pos.address,
        "city_id": pos.city_id,
        "phone": pos.phone,
        "email": pos.email,
        "is_active": pos.is_active
    }