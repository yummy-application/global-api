from database.database import get_connection
def create_restaurant(name, backend_address, password_hash, image=None, location: tuple[float, float] = None):
    with get_connection() as db:
        cursor = db.cursor(buffered=True, dictionary=True)
        if location is not None:
            lat, lon = location
            cursor.execute(
                "INSERT INTO restaurants (restaurant_name, backend_address, restaurant_image, location, password_hash) "
                "VALUES (%(name)s, %(backend_address)s, %(image)s, POINT(%(lat)s, %(lon)s), %(password_hash)s)",
                {
                    "name": name,
                    "backend_address": backend_address,
                    "image": image,
                    "lat": lat,
                    "lon": lon,
                    "password_hash": password_hash
                }
            )
        else:
            cursor.execute(
                "INSERT INTO restaurants (restaurant_name, backend_address, restaurant_image, location, password_hash) "
                "VALUES (%(name)s, %(backend_address)s, %(image)s, NULL, %(password_hash)s)",
                {
                    "name": name,
                    "backend_address": backend_address,
                    "image": image,
                    "password_hash": password_hash
                }
            )
        db.commit()
