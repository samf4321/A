class Configuration:
    def __init__(self, size, f_name, l_name, street, city, state,postal_code, email, phone, number, date, cvv   ):
        # size is men's size

        self.info = {
            "size": size,
            "f_name": f_name,
            "l_name": l_name,
            "street": street,
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "email": email,
            "phone": phone,
            "number": number,
            "date": date,
            "cvv": cvv
        }

    def __getitem__(self, item):
        return self.info[item]

    def __setitem__(self, key, value):
        self[key] = value