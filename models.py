from db import get_db_connection
import hashlib

# POO - ABSTRACCIÓN:
# Clase base para varias secciones del portfolio.
class BaseSection:
    def __init__(self, id=None):
        self._id = id  # POO - ENCAPSULAMIENTO (atributo "privado")

    @property
    def id(self):
        return self._id

    def to_dict(self):
        """Método genérico, ideal para usar en plantillas."""
        return {"id": self._id}


# POO - HERENCIA:
# Clases hijas para cada sección reutilizan la lógica de BaseSection.
class Experience(BaseSection):
    table_name = "experiences"

    def __init__(self, id, role, company, description, year_start, year_end, is_current):
        super().__init__(id)
        self.role = role
        self.company = company
        self.description = description
        self.year_start = year_start
        self.year_end = year_end
        self.is_current = bool(is_current)

    # POO - POLIMORFISMO:
    # Todas las secciones tienen to_dict pero cada una agrega sus cosas.
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "role": self.role,
            "company": self.company,
            "description": self.description,
            "year_start": self.year_start,
            "year_end": self.year_end,
            "is_current": self.is_current,
        })
        return data

    @classmethod
    def all(cls):
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name} ORDER BY year_start DESC;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(**row) for row in rows]

    @classmethod
    def from_id(cls, exp_id):
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name} WHERE id = %s;", (exp_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return cls(**row) if row else None

    def update(self):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(
            f"""UPDATE {self.table_name}
                SET role=%s, company=%s, description=%s,
                    year_start=%s, year_end=%s, is_current=%s
                WHERE id=%s;""",
            (self.role, self.company, self.description,
             self.year_start, self.year_end, int(self.is_current), self.id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def create(cls, role, company, description, year_start, year_end, is_current):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(
            f"""INSERT INTO {cls.table_name}
                (role, company, description, year_start, year_end, is_current)
                VALUES (%s,%s,%s,%s,%s,%s);""",
            (role, company, description, year_start, year_end, int(is_current))
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def delete(cls, exp_id):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {cls.table_name} WHERE id=%s;", (exp_id,))
        conn.commit()
        cursor.close()
        conn.close()


class Education(BaseSection):
    table_name = "education"

    def __init__(self, id, institution, degree, description, year_start, year_end):
        super().__init__(id)
        self.institution = institution
        self.degree = degree
        self.description = description
        self.year_start = year_start
        self.year_end = year_end

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "institution": self.institution,
            "degree": self.degree,
            "description": self.description,
            "year_start": self.year_start,
            "year_end": self.year_end,
        })
        return data

    @classmethod
    def all(cls):
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name} ORDER BY year_start DESC;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(**row) for row in rows]

    @classmethod
    def from_id(cls, edu_id):
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name} WHERE id=%s;", (edu_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return cls(**row) if row else None

    def update(self):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(
            f"""UPDATE {self.table_name}
                SET institution=%s, degree=%s, description=%s,
                    year_start=%s, year_end=%s
                WHERE id=%s;""",
            (self.institution, self.degree, self.description,
             self.year_start, self.year_end, self.id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def create(cls, institution, degree, description, year_start, year_end):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(
            f"""INSERT INTO {cls.table_name}
                (institution, degree, description, year_start, year_end)
                VALUES (%s,%s,%s,%s,%s);""",
            (institution, degree, description, year_start, year_end)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def delete(cls, edu_id):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {cls.table_name} WHERE id=%s;", (edu_id,))
        conn.commit()
        cursor.close()
        conn.close()


class Skill(BaseSection):
    table_name = "skills"

    def __init__(self, id, name, level, type):
        super().__init__(id)
        self.name = name
        self.level = level
        self.type = type

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "name": self.name,
            "level": self.level,
            "type": self.type,
        })
        return data

    @classmethod
    def all(cls):
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name} ORDER BY type, level DESC;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(**row) for row in rows]

    @classmethod
    def from_id(cls, skill_id):
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name} WHERE id=%s;", (skill_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return cls(**row) if row else None

    def update(self):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(
            f"""UPDATE {self.table_name}
                SET name=%s, level=%s, type=%s
                WHERE id=%s;""",
            (self.name, self.level, self.type, self.id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def create(cls, name, level, type):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(
            f"""INSERT INTO {cls.table_name}
                (name, level, type)
                VALUES (%s,%s,%s);""",
            (name, level, type)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def delete(cls, skill_id):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {cls.table_name} WHERE id=%s;", (skill_id,))
        conn.commit()
        cursor.close()
        conn.close()


class Project(BaseSection):
    table_name = "projects"

    def __init__(self, id, name, date_label, description, link):
        super().__init__(id)
        self.name = name
        self.date_label = date_label
        self.description = description
        self.link = link

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "name": self.name,
            "date_label": self.date_label,
            "description": self.description,
            "link": self.link,
        })
        return data

    @classmethod
    def all(cls):
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name} ORDER BY id DESC;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(**row) for row in rows]

    @classmethod
    def from_id(cls, proj_id):
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name} WHERE id=%s;", (proj_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return cls(**row) if row else None

    def update(self):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(
            f"""UPDATE {self.table_name}
                SET name=%s, date_label=%s, description=%s, link=%s
                WHERE id=%s;""",
            (self.name, self.date_label, self.description, self.link, self.id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def create(cls, name, date_label, description, link):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(
            f"""INSERT INTO {cls.table_name}
                (name, date_label, description, link)
                VALUES (%s,%s,%s,%s);""",
            (name, date_label, description, link)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def delete(cls, proj_id):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {cls.table_name} WHERE id=%s;", (proj_id,))
        conn.commit()
        cursor.close()
        conn.close()


class About(BaseSection):
    table_name = "about"

    def __init__(self, id, full_name, title, summary, email, phone, address, profile_image):
        super().__init__(id)
        self.full_name = full_name
        self.title = title
        self.summary = summary
        self.email = email
        self.phone = phone
        self.address = address
        self.profile_image = profile_image

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "full_name": self.full_name,
            "title": self.title,
            "summary": self.summary,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "profile_image": self.profile_image,
        })
        return data

    @classmethod
    def get_single(cls):
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name} LIMIT 1;")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return cls(**row) if row else None

    def update(self):
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(
            f"""UPDATE {self.table_name}
                SET full_name=%s, title=%s, summary=%s,
                    email=%s, phone=%s, address=%s, profile_image=%s
                WHERE id=%s;""",
            (self.full_name, self.title, self.summary,
             self.email, self.phone, self.address,
             self.profile_image, self.id)
        )
        conn.commit()
        cursor.close()
        conn.close()


class SocialLink(BaseSection):
    table_name = "social_links"

    def __init__(self, id, platform, url, icon_class):
        super().__init__(id)
        self.platform = platform
        self.url = url
        self.icon_class = icon_class

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "platform": self.platform,
            "url": self.url,
            "icon_class": self.icon_class
        })
        return data

    @classmethod
    def all(cls):
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name};")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(**row) for row in rows]


class User:
    """
    Modelo simple de usuario para login.
    No uso ORM para que se vea más "manual".
    """
    def __init__(self, id, username, password_hash, full_name):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.full_name = full_name

    @classmethod
    def find_by_username(cls, username):
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s;", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return cls(**row) if row else None

    @staticmethod
    def hash_password(plain_password: str) -> str:
        # hash simple con SHA-256 (para el TP alcanza)
        return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()

    def check_password(self, plain_password: str) -> bool:
        return self.password_hash == self.hash_password(plain_password)
