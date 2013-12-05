BEGIN;

CREATE TABLE person (
    person_id BIGSERIAL PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    title TEXT
);

CREATE TABLE skill (
    skill_id BIGSERIAL PRIMARY KEY,
    skill_name TEXT
);

CREATE TABLE person_skills (
    person_id BIGINT REFERENCES person(person_id),
    skill_id BIGINT REFERENCES skill(skill_id)
);

CREATE TABLE role (
    role_id BIGSERIAL PRIMARY KEY,
    role_name TEXT
);

CREATE TABLE company (
    company_id BIGSERIAL PRIMARY KEY,
    company_name TEXT
);

CREATE TABLE person_jobs (
    person_id BIGINT REFERENCES person(person_id),
    role_id BIGINT REFERENCES role(role_id),
    company_id BIGINT REFERENCES company(company_id)
);

COMMIT;