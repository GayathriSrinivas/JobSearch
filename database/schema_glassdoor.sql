BEGIN;

DROP TABLE g_company CASCADE;
DROP TABLE g_related_company CASCADE;
DROP TABLE g_role CASCADE;
DROP TABLE g_salary CASCADE;

CREATE TABLE g_company (
    company_id BIGSERIAL PRIMARY KEY,
    company_name TEXT,
    revenue TEXT,
    location TEXT,
    ceo TEXT,
    rating INT,
    type TEXT,
    size BIGINT,
    website TEXT,
    ceo_picture TEXT,
    industry TEXT
);

CREATE TABLE g_related_company(
    company_id1 BIGINT REFERENCES g_company(company_id),
    company_id2 BIGINT REFERENCES g_company(company_id)
);

CREATE TABLE g_role(
    role_id BIGSERIAL PRIMARY KEY,
    role_name TEXT
);

CREATE TABLE g_salary(
    company_id BIGINT REFERENCES g_company(company_id),
    role_id BIGINT REFERENCES g_role(role_id),
    mean BIGINT,
    range_low BIGINT,
    range_high BIGINT,
    samples BIGINT
);

COMMIT;