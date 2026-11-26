"""Tests of lab 1.4: one class per task, each one runs a file of queries/."""


class TestSeed:
    """Guard: green from the start. It fails only if seed.sql was changed."""

    def test_ten_members(self, db):
        assert db.execute("SELECT count(*) FROM members;").fetchone() == (10,)


class TestTask1NoPhone:
    def test_members_without_phone(self, check):
        check("01_no_phone.sql", columns=["id", "name"], rows=[
            (2, "Carlos Vega"),
            (4, "Miguel Ccori"),
            (6, "Diego Salas"),
        ])


class TestTask2NewBranch:
    def test_members_to_notify(self, check):
        check("02_new_branch.sql", columns=["id", "name", "district"], rows=[
            (2, "Carlos Vega", "Surquillo"),
            (3, "Lucía Paredes", None),
            (5, "Valeria Ríos", "Barranco"),
            (6, "Diego Salas", None),
            (7, "Fiorella Chávez", "San Isidro"),
            (9, "Camila Torres", "Surquillo"),
            (10, "Andrés Huamán", "Barranco"),
        ])


class TestTask3AmountToPay:
    def test_monthly_amount_of_every_member(self, check):
        check("03_amount_to_pay.sql", columns=["id", "name", "to_pay"], rows=[
            (1, "Rosa Mendoza", 100),
            (2, "Carlos Vega", 120),
            (3, "Lucía Paredes", 100),
            (4, "Miguel Ccori", 100),
            (5, "Valeria Ríos", 120),
            (6, "Diego Salas", 110),
            (7, "Fiorella Chávez", 150),
            (8, "Renzo Quispe", 85),
            (9, "Camila Torres", 120),
            (10, "Andrés Huamán", 150),
        ])


class TestTask4ContactList:
    def test_contact_list(self, check):
        check("04_contact_list.sql", columns=["id", "name", "email"], rows=[
            (1, "Rosa Mendoza", "rosa.mendoza@example.com"),
            (2, "Carlos Vega", "carlos.vega@example.com"),
            (3, "Lucía Paredes", "sin correo"),
            (4, "Miguel Ccori", "sin correo"),
            (5, "Valeria Ríos", "valeria.rios@example.com"),
            (6, "Diego Salas", "diego.salas@example.com"),
            (7, "Fiorella Chávez", "sin correo"),
            (8, "Renzo Quispe", "renzo.quispe@example.com"),
            (9, "Camila Torres", "sin correo"),
            (10, "Andrés Huamán", "andres.huaman@example.com"),
        ])
