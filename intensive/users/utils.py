def normilize_email(email):
    email = email or ""
    email = email.lower()
    try:
        email_name, domain_part = email.strip().rsplit("@", 1)
    except ValueError:
        pass
    else:
        email_name = email_name.split("+", 1)[0]
        domain_part = domain_part.replace("ya.ru", "yandex.ru")
        if domain_part == "gmail.com":
            email_name = email_name.replace(".", "")
        elif domain_part == "yandex.ru":
            email_name = email_name.replace(".", "-")
        email = email_name + "@" + domain_part
    return email
