# Generated by Django 3.1 on 2021-04-04 17:09

from django.db import migrations
from django.db import connection


def automatic_migration():
    with connection.cursor() as cursor:
        cursor.execute(
            '''
                DROP TABLE IF EXISTS ov.companies;
                CREATE TABLE ov.companies (
                    cin bigint,
                    name varchar(255),
                    br_section varchar(255),
                    address_line varchar(255),
                    last_update timestamp,
                    created_at timestamp,
                    updated_at timestamp,
                    PRIMARY KEY(cin)
                );


                INSERT INTO ov.companies (cin, name, br_section, address_line, last_update, created_at, updated_at)
                SELECT insertion_data.cin, insertion_data.corporate_body_name, insertion_data.br_section, 
                CASE
                    WHEN insertion_data.street IS NOT NULL AND insertion_data.postal_code IS NOT NULL AND insertion_data.city IS NOT NULL
                    THEN CONCAT(insertion_data.street, ', ', insertion_data.postal_code, ' ', insertion_data.city)
                    ELSE NULL
                END AS address_line, insertion_data.updated_at, NOW()::timestamp, NOW()::timestamp
                FROM (
                    SELECT rank_filter.* FROM (
                        SELECT cin, corporate_body_name, br_section, street, postal_code, city, updated_at,
                        rank() OVER (PARTITION BY cin ORDER BY updated_at DESC)
                        FROM (			
                            (
                                SELECT cin, corporate_body_name, br_section, street, postal_code, city, updated_at
                                FROM ov.or_podanie_issues
                                WHERE cin IS NOT NULL
                            )
                            UNION ALL
                            (
                                SELECT cin, corporate_body_name, br_section, street, postal_code, city, updated_at
                                FROM ov.likvidator_issues
                                WHERE cin IS NOT NULL
                            )
                            UNION ALL
                            (
                                SELECT cin, corporate_body_name, NULL AS br_section, street, postal_code, city, updated_at
                                FROM ov.konkurz_vyrovnanie_issues
                                WHERE cin IS NOT NULL
                            )
                            UNION ALL
                            (
                                SELECT cin, corporate_body_name, br_section, street, postal_code, city, updated_at
                                FROM ov.znizenie_imania_issues
                                WHERE cin IS NOT NULL
                            )
                            UNION ALL
                            (
                                SELECT cin, corporate_body_name, NULL AS br_section, street, postal_code, city, updated_at
                                FROM ov.konkurz_restrukturalizacia_actors
                                WHERE cin IS NOT NULL
                            )
                        ) AS union_table
                    ) AS rank_filter WHERE RANK = 1
                ) AS insertion_data;

                ALTER TABLE ov.or_podanie_issues
                    DROP COLUMN IF EXISTS company_id;
                ALTER TABLE ov.or_podanie_issues
                    DROP CONSTRAINT IF EXISTS fkey_company_id;
                ALTER TABLE ov.or_podanie_issues
                    ADD COLUMN company_id bigint;
                UPDATE ov.or_podanie_issues
                    SET company_id = cin
                    WHERE cin IS NOT NULL;
                ALTER TABLE ov.or_podanie_issues
                    ADD CONSTRAINT fkey_company_id
                    FOREIGN KEY (company_id)
                    REFERENCES ov.companies(cin);

                ALTER TABLE ov.likvidator_issues
                    DROP COLUMN IF EXISTS company_id;
                ALTER TABLE ov.likvidator_issues
                    DROP CONSTRAINT IF EXISTS fkey_company_id;
                ALTER TABLE ov.likvidator_issues
                    ADD COLUMN company_id bigint;
                UPDATE ov.likvidator_issues
                    SET company_id = cin
                    WHERE cin IS NOT NULL;
                ALTER TABLE ov.likvidator_issues
                    ADD CONSTRAINT fkey_company_id
                    FOREIGN KEY (company_id)
                    REFERENCES ov.companies(cin);

                ALTER TABLE ov.konkurz_vyrovnanie_issues
                    DROP COLUMN IF EXISTS company_id;
                ALTER TABLE ov.konkurz_vyrovnanie_issues
                    DROP CONSTRAINT IF EXISTS fkey_company_id;
                ALTER TABLE ov.konkurz_vyrovnanie_issues
                    ADD COLUMN company_id bigint;
                UPDATE ov.konkurz_vyrovnanie_issues
                    SET company_id = cin
                    WHERE cin IS NOT NULL;
                ALTER TABLE ov.konkurz_vyrovnanie_issues
                    ADD CONSTRAINT fkey_company_id
                    FOREIGN KEY (company_id)
                    REFERENCES ov.companies(cin);

                ALTER TABLE ov.znizenie_imania_issues
                    DROP COLUMN IF EXISTS company_id;
                ALTER TABLE ov.znizenie_imania_issues
                    DROP CONSTRAINT IF EXISTS fkey_company_id;
                ALTER TABLE ov.znizenie_imania_issues
                    ADD COLUMN company_id bigint;
                UPDATE ov.znizenie_imania_issues
                    SET company_id = cin
                    WHERE cin IS NOT NULL;
                ALTER TABLE ov.znizenie_imania_issues
                    ADD CONSTRAINT fkey_company_id
                    FOREIGN KEY (company_id)
                    REFERENCES ov.companies(cin);

                ALTER TABLE ov.konkurz_restrukturalizacia_actors
                    DROP COLUMN IF EXISTS company_id;
                ALTER TABLE ov.konkurz_restrukturalizacia_actors
                    DROP CONSTRAINT IF EXISTS fkey_company_id;
                ALTER TABLE ov.konkurz_restrukturalizacia_actors
                    ADD COLUMN company_id bigint;
                UPDATE ov.konkurz_restrukturalizacia_actors
                    SET company_id = cin
                    WHERE cin IS NOT NULL;
                ALTER TABLE ov.konkurz_restrukturalizacia_actors
                    ADD CONSTRAINT fkey_company_id
                    FOREIGN KEY (company_id)
                    REFERENCES ov.companies(cin);
            '''
        )
    connection.commit()


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        # migrations.RunSQL(automatic_migration(), hints={
        #                   'target_db': 'default'})
    ]