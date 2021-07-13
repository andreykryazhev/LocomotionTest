import os
import psycopg2

HOST = 'localhost'
DBNAME = 'locomotion'
USER = 'postgres'
PSWD = 'root'
FILIALS_CSV_PATH = os.path.abspath('filials.csv')
STAKES_CSV_PATH = os.path.abspath('stakes.csv')
MILEAGE_CSV_PATH = os.path.abspath('mileage.csv')


db=psycopg2.connect(host=HOST, dbname=DBNAME, user=USER, password=PSWD)
cur = db.cursor()

years = ['y20{:02} INTEGER'.format(x) for x in range(17, 55)]

cur.execute('''

    begin;    
    DELETE FROM loco_app_mileage;
    DELETE FROM loco_app_filials;
    DELETE FROM loco_app_series;

    COPY loco_app_filials(name) FROM '{}' DELIMITER ';' CSV;
    UPDATE loco_app_filials SET name = TRIM(name);


    COPY loco_app_series(name, stake) FROM '{}' DELIMITER ';' CSV;
    UPDATE loco_app_series SET name = TRIM(name);

    CREATE TABLE tmp (
        filial VARCHAR(50),
        serie VARCHAR(50),
        {}
    );
    UPDATE tmp SET serie = TRIM(serie);
    COPY tmp FROM '{}' DELIMITER ';' CSV;

    CREATE OR REPLACE FUNCTION convert_locomotion_xklskdsj() RETURNS VOID AS $$
    DECLARE
        r RECORD;
    BEGIN

        FOR r IN (
            SELECT
                column_name,
                substring(column_name, '.([0-9]*)') as "year"
            FROM information_schema.columns
            WHERE table_name = 'tmp' AND column_name LIKE 'y%'
        ) LOOP
            EXECUTE format('
                INSERT INTO loco_app_mileage(filial_id, serie_id, serie_name, date, value)
                    SELECT
                        loco_app_filials.id,
                        loco_app_series.id,
                        COALESCE(loco_app_series.name, tmp.serie),
                        ''%s-01-01''::date,
                        %I
                    FROM tmp
                    LEFT JOIN loco_app_filials ON loco_app_filials.name = TRIM(tmp.filial)
                    LEFT JOIN loco_app_series ON loco_app_series.name = TRIM(tmp.serie)',
                r.year, r.column_name);
        END LOOP;
        RETURN;
    END
    $$ LANGUAGE plpgsql;

    select convert_locomotion_xklskdsj();
    DROP FUNCTION convert_locomotion_xklskdsj;
    DROP TABLE tmp;
    commit;
    '''.format(
        FILIALS_CSV_PATH, STAKES_CSV_PATH, ','.join(years), MILEAGE_CSV_PATH
    )
)

db.commit()
cur.close()
db.close()