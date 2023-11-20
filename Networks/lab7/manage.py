#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.db import connection



def main():
    """Run administrative tasks."""
    drop_trigger = 'DROP TRIGGER IF EXISTS price_change_trigger'
    trigger_sql = """
    CREATE TRIGGER IF NOT EXISTS price_change_trigger
    AFTER UPDATE OF price ON products_product
    BEGIN
        INSERT INTO products_pricechangelog (code ,new_price, change_date, company, name)
        SELECT  NEW.code, NEW.price, CURRENT_TIMESTAMP, NEW.company, NEW.name;
    END;
    """

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab2.settings')


    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
